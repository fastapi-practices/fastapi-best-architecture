import os

from typing import Any

import rtoml

from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefinedType
from pydantic_settings import PydanticBaseSettingsSource

from backend.core.path_conf import PLUGIN_DIR


class PluginSettingsSource(PydanticBaseSettingsSource):
    """从所有插件的 plugin.toml 加载配置的自定义配置源"""

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        """获取单个字段的值"""
        # 不在这里实现，使用 __call__ 批量加载
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        """加载所有插件配置"""
        merged_settings: dict[str, Any] = {}

        for item in os.listdir(PLUGIN_DIR):
            item_path = PLUGIN_DIR / item
            if not os.path.isdir(item_path):
                continue
            if '__init__.py' not in os.listdir(item_path):
                continue
            toml_path = item_path / 'plugin.toml'
            if toml_path.exists():
                with open(toml_path, encoding='utf-8') as f:
                    config = rtoml.load(f)
                    plugin_settings = config.get('settings', {})
                    merged_settings.update(plugin_settings)

        filtered_settings: dict[str, Any] = {}
        for key, value in merged_settings.items():
            field_info = self.settings_cls.model_fields.get(key)
            if field_info is not None:
                if isinstance(field_info.default, PydanticUndefinedType):
                    filtered_settings[key] = value
            else:
                filtered_settings[key] = value

        return filtered_settings
