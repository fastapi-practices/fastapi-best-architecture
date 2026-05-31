import io
import os
import shutil
import tempfile
import zipfile

from collections.abc import Sequence

import anyio

from anyio import open_file
from pydantic.alias_generators import to_pascal
from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from backend.common.exception import errors
from backend.core.conf import settings
from backend.core.path_conf import BASE_PATH
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.crud.crud_gen import gen_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam
from backend.plugin.code_generator.schema.column import CreateGenColumnInternalParam
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.column_service import gen_column_service
from backend.plugin.code_generator.utils.format_code import format_python_code
from backend.plugin.code_generator.utils.gen_template import gen_template
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic
from backend.utils.locks import acquire_distributed_reload_lock


class GenService:
    """代码生成服务类"""

    @staticmethod
    async def get_tables(*, db: AsyncSession, table_schema: str) -> Sequence[RowMapping]:
        """
        获取指定 schema 下的所有表名

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :return:
        """
        return await gen_dao.get_all_tables(db, table_schema)

    @staticmethod
    async def import_business_and_model(*, db: AsyncSession, obj: ImportParam) -> None:
        """
        导入业务和模型列数据

        :param db: 数据库会话
        :param obj: 导入参数对象
        :return:
        """
        if settings.ENVIRONMENT != 'dev':
            raise errors.ForbiddenError(msg='禁止在非开发环境下导入代码生成业务')

        table_info = await gen_dao.get_table(db, obj.table_schema, obj.table_name)
        if not table_info:
            raise errors.NotFoundError(msg='数据库表不存在')

        business_info = await gen_business_dao.get_by_name(db, obj.table_name)
        if business_info:
            raise errors.ConflictError(msg='已存在相同数据库表业务')

        table_name = table_info['table_name']
        doc_comment = (
            table_info['table_comment'][:-1]
            if table_info['table_comment'][-1] == '表'
            else table_info['table_comment'] or table_name.split('_')[-1]
        )
        new_business = GenBusiness(
            **CreateGenBusinessParam(
                app_name=obj.app,
                table_name=table_name,
                doc_comment=doc_comment,
                table_comment=table_info['table_comment'],
                class_name=to_pascal(table_name),
                schema_name=to_pascal(table_name),
                filename=table_name,
                tag=doc_comment,
            ).model_dump(),
        )
        db.add(new_business)
        await db.flush()

        column_info = await gen_dao.get_all_columns(db, obj.table_schema, table_name)
        gen_columns = []
        for column in column_info:
            column_type = column['column_type'].split('(')[0].upper()
            pd_type = sql_type_to_pydantic(column_type)
            gen_columns.append(
                CreateGenColumnInternalParam(
                    name=column['column_name'],
                    comment=column['column_comment'],
                    type=column_type,
                    sort=column['sort'],
                    length=column['column_type'].split('(')[1][:-1]
                    if pd_type == 'str' and '(' in column['column_type']
                    else 0,
                    is_pk=column['is_pk'],
                    is_nullable=column['is_nullable'],
                    gen_business_id=new_business.id,
                    pd_type=pd_type,
                ),
            )
        await gen_column_dao.bulk_create(db, gen_columns)

    @staticmethod
    async def _render_tpl_code(*, db: AsyncSession, business: GenBusiness) -> dict[str, str]:
        """
        渲染模板代码

        :param db: 数据库会话
        :param business: 业务对象
        :return:
        """
        gen_models = await gen_column_service.get_columns(db=db, business_id=business.id)
        if not gen_models:
            raise errors.NotFoundError(msg='代码生成模型表为空')

        gen_vars = gen_template.get_vars(business, gen_models)
        template_mapping = gen_template.get_template_path_mapping(business)

        rendered_codes = {}
        for template_path, output_path in template_mapping.items():
            code = await gen_template.get_template(template_path).render_async(**gen_vars)
            if output_path.endswith('.py'):
                code = await format_python_code(code)
            rendered_codes[output_path] = code

        return rendered_codes

    @staticmethod
    async def _inject_app_router(*, app_name: str, write: bool = True) -> str | None:
        """
        注入应用路由

        :param app_name:
        :param write: 是否写入文件
        :return:
        """
        app_root_router = BASE_PATH / 'app' / 'router.py'

        async with await open_file(app_root_router, 'r', encoding='utf-8') as f:
            content = await f.read()

        import_line = f'from backend.app.{app_name}.api.router import v1 as {app_name}_v1'
        include_line = f'router.include_router({app_name}_v1)'
        has_import = import_line in content  # type: ignore
        has_include = include_line in content  # type: ignore

        if has_import and has_include:
            return None

        if not has_import:
            content = f'{import_line}\n{content}'
        if not has_include:
            content = f'{content}\n{include_line}'

        content = await format_python_code(content)

        if write:
            async with await open_file(app_root_router, 'w', encoding='utf-8') as f:
                await f.write(content)

        return content

    async def preview(self, *, db: AsyncSession, pk: int) -> dict[str, bytes]:
        """
        预览生成的代码

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """
        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        codes = {}
        backend_path = 'fastapi-best-architecture/backend/app/'

        init_files = gen_template.get_init_files(business)
        for filepath, content in init_files.items():
            codes[f'{backend_path}{filepath}'] = content.encode('utf-8')

        rendered_codes = await self._render_tpl_code(db=db, business=business)
        for filepath, code in rendered_codes.items():
            codes[f'{backend_path}{filepath}'] = code.encode('utf-8')

        app_router_content = await self._inject_app_router(app_name=business.app_name, write=False)
        if app_router_content:
            codes[f'{backend_path}router.py'] = app_router_content.encode('utf-8')

        return codes

    @staticmethod
    async def get_generate_path(*, db: AsyncSession, pk: int) -> list[str]:
        """
        获取代码生成路径

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """
        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        gen_path = business.gen_path or '<project_root>/backend/app'
        paths = []

        init_files = gen_template.get_init_files(business)
        paths.extend(os.path.join(gen_path, *filepath.split('/')) for filepath in init_files.keys())

        template_mapping = gen_template.get_template_path_mapping(business)
        paths.extend(os.path.join(gen_path, *filepath.split('/')) for filepath in template_mapping.values())

        return paths

    async def generate(self, *, db: AsyncSession, pk: int) -> str:
        """
        生成代码文件

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """
        if settings.ENVIRONMENT != 'dev':
            raise errors.ForbiddenError(msg='禁止在非开发环境下生成代码')

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        gen_path = business.gen_path or str(BASE_PATH / 'app')

        async with acquire_distributed_reload_lock():
            with tempfile.TemporaryDirectory() as tmp_dir:
                all_files = {}
                init_files = gen_template.get_init_files(business)
                all_files.update(init_files)
                rendered_codes = await self._render_tpl_code(db=db, business=business)
                all_files.update(rendered_codes)

                for filepath, content in all_files.items():
                    full_path = os.path.join(tmp_dir, *filepath.split('/'))
                    code_folder = anyio.Path(full_path).parent
                    await code_folder.mkdir(parents=True, exist_ok=True)
                    async with await open_file(full_path, 'w', encoding='utf-8') as f:
                        await f.write(content)

                for item in os.listdir(tmp_dir):
                    src = os.path.join(tmp_dir, item)
                    dst = os.path.join(gen_path, item)
                    src_path = anyio.Path(src)
                    if await src_path.is_dir():
                        await run_in_threadpool(shutil.copytree, src, dst, dirs_exist_ok=True)
                    else:
                        await run_in_threadpool(shutil.copy2, src, dst)

            await self._inject_app_router(app_name=business.app_name)

        return gen_path

    async def download(self, *, db: AsyncSession, pk: int) -> io.BytesIO:
        """
        下载生成的代码

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """
        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        all_files = {}
        init_files = gen_template.get_init_files(business)
        all_files.update(init_files)
        rendered_codes = await self._render_tpl_code(db=db, business=business)
        all_files.update(rendered_codes)

        app_router_content = await self._inject_app_router(app_name=business.app_name, write=False)
        if app_router_content:
            all_files['router.py'] = app_router_content

        bio = io.BytesIO()
        with zipfile.ZipFile(bio, 'w') as zf:
            for filepath, content in all_files.items():
                zf.writestr(filepath, content)

        bio.seek(0)
        return bio


gen_service: GenService = GenService()
