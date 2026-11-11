import hashlib
import json
import operator

from fastapi import Request

from backend.core.conf import settings


def http_cache_key(request: Request, eviction_group: str = '', prefix: str = '') -> str:
    """
    为 SDK HTTP 缓存隔离 JWT 用户、站点、语言及查询参数

    :param request: HTTP 请求
    :param eviction_group: SDK 缓存失效组
    :param prefix: SDK 缓存键前缀
    :return:
    """
    user_id = getattr(request.scope.get('user'), 'id', None)
    dimensions = [
        str(user_id) if user_id is not None else 'anonymous',
        request.url.scheme,
        request.url.netloc,
        request.url.path,
        request.headers.get('accept-language', settings.I18N_DEFAULT_LANGUAGE),
        request.headers.get('accept', ''),
        sorted(request.query_params.multi_items(), key=operator.itemgetter(0)),
    ]
    digest = hashlib.sha256(json.dumps(dimensions, ensure_ascii=True).encode()).hexdigest()
    return f'{prefix}:{{{eviction_group}}}:{digest}'
