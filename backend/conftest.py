from collections.abc import Generator

import pytest

from starlette.testclient import TestClient

from backend.core.conf import settings
from backend.database.db import get_db, get_db_transaction
from backend.main import app
from backend.tests.utils.db import override_get_db, override_get_db_transaction

# 重载数据库
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_db_transaction] = override_get_db_transaction


# Test data
PYTEST_USERNAME = 'admin'
PYTEST_PASSWORD = '123456'
PYTEST_BASE_URL = f'http://testserver{settings.FASTAPI_API_V1_PATH}'


@pytest.fixture(scope='session')
def client() -> Generator:
    with TestClient(app, base_url=PYTEST_BASE_URL) as c:
        yield c


@pytest.fixture(scope='module')
def token_headers(client: TestClient) -> Generator[dict[str, str], None, None]:
    params = {
        'username': PYTEST_USERNAME,
        'password': PYTEST_PASSWORD,
    }
    response = client.post('/auth/login/swagger', params=params)
    response.raise_for_status()
    token_type = response.json()['token_type']
    access_token = response.json()['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    yield headers
    client.post('/auth/logout', headers=headers)
