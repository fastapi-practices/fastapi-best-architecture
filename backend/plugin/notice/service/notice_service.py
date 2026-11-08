from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.notice.crud.crud_notice import notice_dao
from backend.plugin.notice.model import Notice
from backend.plugin.notice.schema.notice import CreateNoticeParam, DeleteNoticeParam, UpdateNoticeParam


class NoticeService:
    """通知公告服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Notice:
        """
        获取通知公告

        :param db: 数据库会话
        :param pk: 通知公告 ID
        :return:
        """
        notice = await notice_dao.get(db, pk)
        if not notice:
            raise errors.NotFoundError(msg='通知公告不存在')
        return notice

    @staticmethod
    async def get_list(db: AsyncSession, title: str | None, type: int | None, status: int | None) -> dict[str, Any]:
        """
        获取通知公告列表

        :param db: 数据库会话
        :param title: 通知公告标题
        :param type: 通知公告类型
        :param status: 通知公告状态
        :return:
        """
        notice_select = await notice_dao.get_select(title, type, status)
        return await paging_data(db, notice_select)

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[Notice]:
        """
        获取所有通知公告

        :param db: 数据库会话
        :return:
        """
        notices = await notice_dao.get_all(db)
        return notices

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateNoticeParam) -> None:
        """
        创建通知公告

        :param db: 数据库会话
        :param obj: 创建通知公告参数
        :return:
        """
        await notice_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateNoticeParam) -> int:
        """
        更新通知公告

        :param db: 数据库会话
        :param pk: 通知公告 ID
        :param obj: 更新通知公告参数
        :return:
        """
        notice = await notice_dao.get(db, pk)
        if not notice:
            raise errors.NotFoundError(msg='通知公告不存在')
        count = await notice_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteNoticeParam) -> int:
        """
        批量删除通知公告

        :param db: 数据库会话
        :param obj: 通知公告 ID 列表
        :return:
        """
        count = await notice_dao.delete(db, obj.pks)
        return count


notice_service: NoticeService = NoticeService()
