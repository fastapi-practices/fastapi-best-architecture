from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase
from backend.plugin.notice.enums import NoticeType


class NoticeQueryParam(SchemaBase):
    """通知公告查询参数"""

    title: str | None = Field(None, description='标题')
    type: int | None = Field(None, description='类型')
    status: int | None = Field(None, description='状态')


class NoticeSchemaBase(SchemaBase):
    """通知公告基础模型"""

    title: str = Field(description='标题')
    type: NoticeType = Field(description='类型（0：通知、1：公告）')
    status: StatusType = Field(description='状态（0：隐藏、1：显示）')
    content: str = Field(description='内容')


class CreateNoticeParam(NoticeSchemaBase):
    """创建通知公告参数"""


class UpdateNoticeParam(NoticeSchemaBase):
    """更新通知公告参数"""


class DeleteNoticeParam(SchemaBase):
    """删除通知公告参数"""

    pks: list[int] = Field(description='通知公告 ID 列表')


class GetNoticeDetail(NoticeSchemaBase):
    """通知公告详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='通知公告 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
