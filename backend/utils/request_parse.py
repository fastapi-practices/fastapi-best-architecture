import ipaddress

import httpx
import ip2region.searcher as ip2region_xdb
import ip2region.util as ip2region_util

from fastapi import Request
from user_agents import parse

from backend.common.dataclasses import IpInfo, UserAgentInfo
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import STATIC_DIR
from backend.database.redis import redis_client


def get_request_ip(request: Request) -> str:
    """
    获取请求的 IP 地址

    :param request: FastAPI 请求对象
    :return:
    """
    real = request.headers.get('X-Real-IP')
    if real:
        return real

    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0]

    if request.client is None:
        return '127.0.0.1'

    # 忽略 pytest
    if request.client.host == 'testclient':
        return '127.0.0.1'

    return request.client.host


async def get_location_online(ip: str) -> dict | None:
    """
    在线获取 IP 地址属地，无法保证可用性，准确率较高

    :param ip: IP 地址
    :return:
    """
    async with httpx.AsyncClient(timeout=3) as client:
        try:
            response = await client.get(f'http://ip-api.com/json/{ip}?lang=zh-CN')
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            log.error(f'在线获取 IP 地址属地失败，错误信息：{e}')
            return None


# 离线 IP 搜索器（数据将缓存到内存，缓存大小取决于 IP 数据文件大小）
__c_buffer_v4: bytes = ip2region_util.load_content_from_file(STATIC_DIR / 'ip2region_v4.xdb')
__xdb_searcher_v4: ip2region_xdb.Searcher = ip2region_xdb.new_with_buffer(ip2region_util.IPv4, __c_buffer_v4)
__c_buffer_v6: bytes = ip2region_util.load_content_from_file(STATIC_DIR / 'ip2region_v6.xdb')
__xdb_searcher_v6: ip2region_xdb.Searcher = ip2region_xdb.new_with_buffer(ip2region_util.IPv6, __c_buffer_v6)


def get_location_offline(ip: str) -> dict | None:
    """
    离线获取 IP 地址属地，无法保证准确率，100% 可用

    :param ip: IP 地址
    :return:
    """
    try:
        ip_address = ipaddress.ip_address(ip)
        # IPv4 映射的 IPv6 地址（::ffff:a.b.c.d）按 IPv4 查询
        if isinstance(ip_address, ipaddress.IPv6Address) and ip_address.ipv4_mapped:
            ip_address = ip_address.ipv4_mapped
        searcher = __xdb_searcher_v6 if ip_address.version == 6 else __xdb_searcher_v4
        data = searcher.search(str(ip_address))
        # 数据文件未收录该地址（例如 ::1）时返回空字符串
        if not data:
            return None
        country, region_name, city, *_ = data.split('|')
    except Exception as e:
        log.error(f'离线获取 IP 地址属地失败：{e}')
        return None
    else:
        return {
            'country': country if country != '0' else None,
            'regionName': region_name if region_name != '0' else None,
            'city': city if city != '0' else None,
        }


async def parse_ip_info(request: Request) -> IpInfo:
    """
    解析请求的 IP 信息

    :param request: FastAPI 请求对象
    :return:
    """
    country, region, city = None, None, None
    ip = get_request_ip(request)
    location = await redis_client.get(f'{settings.IP_LOCATION_REDIS_PREFIX}:{ip}')
    if location:
        country, region, city = location.split('|')
        return IpInfo(ip=ip, country=country, region=region, city=city)

    location_info = None
    if settings.IP_LOCATION_PARSE == 'online':
        location_info = await get_location_online(ip)
    elif settings.IP_LOCATION_PARSE == 'offline':
        location_info = get_location_offline(ip)

    if location_info:
        country = location_info.get('country')
        region = location_info.get('regionName')
        city = location_info.get('city')
        await redis_client.set(
            f'{settings.IP_LOCATION_REDIS_PREFIX}:{ip}',
            f'{country}|{region}|{city}',
            ex=settings.IP_LOCATION_EXPIRE_SECONDS,
        )
    return IpInfo(ip=ip, country=country, region=region, city=city)


def parse_user_agent_info(request: Request) -> UserAgentInfo:
    """
    解析请求的用户代理信息

    :param request: FastAPI 请求对象
    :return:
    """
    os, browser, device = None, None, None
    user_agent = request.headers.get('User-Agent')
    if user_agent:
        user_agent_ = parse(user_agent)
        os = user_agent_.get_os()
        browser = user_agent_.get_browser()
        device = user_agent_.get_device()
    return UserAgentInfo(user_agent=user_agent, device=device, os=os, browser=browser)
