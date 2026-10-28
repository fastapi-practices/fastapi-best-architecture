from typing import Any

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.model import Dept
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam
from backend.common.exception import errors
from backend.common.i18n import t
from backend.utils.build_tree import get_tree_data


class DeptService:
    """部门服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Dept:
        """
        获取部门详情

        :param db: 数据库会话
        :param pk: 部门 ID
        :return:
        """

        dept = await dept_dao.get(db, pk)
        if not dept:
            raise errors.NotFoundError(msg=t('error.dept.not_found'))
        return dept

    @staticmethod
    async def get_tree(
        *,
        db: AsyncSession,
        data_filter: ColumnElement[bool],
        name: str | None,
        leader: str | None,
        phone: str | None,
        status: int | None,
    ) -> list[dict[str, Any]]:
        """
        获取部门树形结构

        :param db: 数据库会话
        :param data_filter: 请求用户
        :param name: 部门名称
        :param leader: 部门负责人
        :param phone: 联系电话
        :param status: 状态
        :return:
        """
        dept_select = await dept_dao.get_all(db, data_filter, name, leader, phone, status)
        tree_data = get_tree_data(dept_select)
        return tree_data

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDeptParam) -> None:
        """
        创建部门

        :param db: 数据库会话
        :param obj: 部门创建参数
        :return:
        """
        dept = await dept_dao.get_by_name(db, obj.name)
        if dept:
            raise errors.ConflictError(msg=t('error.dept.name_exists'))
        if obj.parent_id is not None:
            parent_dept = await dept_dao.get(db, obj.parent_id)
            if not parent_dept:
                raise errors.NotFoundError(msg=t('error.dept.parent_not_found'))
        await dept_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDeptParam) -> int:
        """
        更新部门

        :param db: 数据库会话
        :param pk: 部门 ID
        :param obj: 部门更新参数
        :return:
        """
        dept = await dept_dao.get(db, pk)
        if not dept:
            raise errors.NotFoundError(msg=t('error.dept.not_found'))
        if dept.name != obj.name and await dept_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg=t('error.dept.name_exists'))
        if obj.parent_id:
            parent_dept = await dept_dao.get(db, obj.parent_id)
            if not parent_dept:
                raise errors.NotFoundError(msg=t('error.dept.parent_not_found'))
        if obj.parent_id == dept.id:
            raise errors.ForbiddenError(msg=t('error.dept.parent_self'))
        count = await dept_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除部门

        :param db: 数据库会话
        :param pk: 部门 ID
        :return:
        """
        dept = await dept_dao.get_join(db, pk)
        if not dept:
            raise errors.NotFoundError(msg=t('error.dept.not_found'))
        if dept.users:
            raise errors.ConflictError(msg=t('error.dept.has_users'))
        children = await dept_dao.get_children(db, pk)
        if children:
            raise errors.ConflictError(msg=t('error.dept.has_children'))
        count = await dept_dao.delete(db, pk)
        return count


dept_service: DeptService = DeptService()
