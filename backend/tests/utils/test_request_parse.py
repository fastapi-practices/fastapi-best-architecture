from unittest.mock import Mock

import pytest

from backend.utils import request_parse


def test_get_location_offline_skips_ipv6(monkeypatch: pytest.MonkeyPatch) -> None:
    searcher = Mock()
    monkeypatch.setattr(request_parse, '__xdb_searcher', searcher)

    assert request_parse.get_location_offline('2a10:480:200::30a3') is None

    searcher.search.assert_not_called()


def test_get_location_offline_keeps_ipv4_lookup(monkeypatch: pytest.MonkeyPatch) -> None:
    searcher = Mock()
    searcher.search.return_value = '中国|广东省|广州市|电信'
    monkeypatch.setattr(request_parse, '__xdb_searcher', searcher)

    assert request_parse.get_location_offline('1.1.1.1') == {
        'country': '中国',
        'regionName': '广东省',
        'city': '广州市',
    }
    searcher.search.assert_called_once_with('1.1.1.1')
