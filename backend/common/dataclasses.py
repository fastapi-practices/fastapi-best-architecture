import dataclasses

from datetime import datetime
from typing import Any

from fastapi import Response

from backend.common.enums import StatusType


@dataclasses.dataclass
class IpInfo:
    ip: str
    country: str | None
    region: str | None
    city: str | None


@dataclasses.dataclass
class UserAgentInfo:
    user_agent: str | None
    os: str | None
    browser: str | None
    device: str | None


@dataclasses.dataclass
class RequestCallNext:
    code: str
    msg: str
    status: StatusType
    err: Exception | None
    response: Response


@dataclasses.dataclass
class AccessToken:
    access_token: str
    access_token_expire_time: datetime
    session_uuid: str


@dataclasses.dataclass
class RefreshToken:
    refresh_token: str
    refresh_token_expire_time: datetime


@dataclasses.dataclass
class NewToken:
    new_access_token: str
    new_access_token_expire_time: datetime
    new_refresh_token: str
    new_refresh_token_expire_time: datetime
    session_uuid: str


@dataclasses.dataclass
class TokenPayload:
    user_id: int
    session_uuid: str
    expire_time: datetime


@dataclasses.dataclass
class UploadUrl:
    url: str


@dataclasses.dataclass
class SnowflakeInfo:
    timestamp: int
    datetime: str
    datacenter_id: int
    worker_id: int
    sequence: int


@dataclasses.dataclass(slots=True)
class PluginEntry:
    name: str
    depends_on: list[str] | None = None
    extend: str | None = None
    routers: list[str] | None = None
    api: dict[str, Any] | None = None
