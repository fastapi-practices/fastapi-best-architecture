from collections.abc import Sequence

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic.alias_generators import to_pascal

from backend.common.enums import PrimaryKeyType
from backend.core.conf import settings
from backend.plugin.code_generator.model import CodeGenBusiness, CodeGenColumn
from backend.plugin.code_generator.path_conf import JINJA2_TEMPLATE_DIR
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_sqlalchemy_name
from backend.utils.snowflake import snowflake
from backend.utils.timezone import timezone


class GenTemplate:
    def __init__(self) -> None:
        """初始化模板生成器"""
        self.env = Environment(
            loader=FileSystemLoader(JINJA2_TEMPLATE_DIR),
            autoescape=select_autoescape(enabled_extensions=['jinja']),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            enable_async=True,
        )
        self.env.filters['sqlalchemy_type'] = sql_type_to_sqlalchemy_name
        self.init_content = ''

    def get_template(self, jinja_file: str) -> Template:
        """
        获取 Jinja2 模板对象

        :param jinja_file: Jinja2 模板文件路径
        :return:
        """
        return self.env.get_template(jinja_file)

    @staticmethod
    def get_template_path_mapping(business: CodeGenBusiness) -> dict[str, str]:
        """
        获取模板文件到生成文件的路径映射

        :param business: 代码生成业务对象
        :return:
        """
        app_name = business.app_name
        filename = business.filename
        api_version = business.api_version
        pk_suffix = '_snowflake' if settings.DATABASE_PK_MODE == 'snowflake' else ''

        return {
            'python/api.jinja': f'{app_name}/api/{api_version}/{filename}.py',
            'python/router.jinja': f'{app_name}/api/router.py',
            'python/crud.jinja': f'{app_name}/crud/crud_{filename}.py',
            'python/model.jinja': f'{app_name}/model/{filename}.py',
            'python/schema.jinja': f'{app_name}/schema/{filename}.py',
            'python/service.jinja': f'{app_name}/service/{filename}_service.py',
            f'sql/mysql/init{pk_suffix}.jinja': f'{app_name}/sql/mysql/init{pk_suffix}.sql',
            f'sql/postgresql/init{pk_suffix}.jinja': f'{app_name}/sql/postgresql/init{pk_suffix}.sql',
        }

    def get_init_files(self, business: CodeGenBusiness) -> dict[str, str]:
        """
        获取需要生成的 __init__.py 文件及其内容

        :param business: 业务对象
        :return:
        """
        app_name = business.app_name
        table_name = business.table_name
        class_name = business.class_name or to_pascal(table_name)
        filename = business.filename

        return {
            f'{app_name}/__init__.py': self.init_content,
            f'{app_name}/api/__init__.py': self.init_content,
            f'{app_name}/api/{business.api_version}/__init__.py': self.init_content,
            f'{app_name}/crud/__init__.py': self.init_content,
            f'{app_name}/model/__init__.py': (
                f'{self.init_content}from backend.app.{app_name}.model.{filename} import {class_name} as {class_name}\n'
            ),
            f'{app_name}/schema/__init__.py': self.init_content,
            f'{app_name}/service/__init__.py': self.init_content,
        }

    @staticmethod
    def get_vars(
        business: CodeGenBusiness, models: Sequence[CodeGenColumn]
    ) -> dict[str, str | Sequence[CodeGenColumn]]:
        """
        获取模板变量

        :param business: 代码生成业务对象
        :param models: 代码生成模型对象列表
        :return:
        """
        vars_dict = {
            'app_name': business.app_name,
            'table_name': business.table_name,
            'doc_comment': business.doc_comment,
            'table_comment': business.table_comment,
            'class_name': business.class_name,
            'schema_name': business.schema_name,
            'filename': business.filename,
            'datetime_mixin': business.datetime_mixin,
            'api_version': business.api_version,
            'tag': business.tag,
            'permission': business.table_name.replace('_', ':'),
            'database_type': settings.DATABASE_TYPE,
            'models': models,
            'model_types': [model.type for model in models],
            'now': timezone.now(),
        }

        if PrimaryKeyType.snowflake == settings.DATABASE_PK_MODE:
            vars_dict['parent_menu_id'] = snowflake.generate()
            vars_dict['button_ids'] = [snowflake.generate() for _ in range(4)]

        return vars_dict


gen_template: GenTemplate = GenTemplate()
