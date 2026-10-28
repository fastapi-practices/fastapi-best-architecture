import glob
import json

from pathlib import Path
from typing import Any

import yaml

from starlette_context.errors import ContextDoesNotExistError

from backend.common.context import ctx
from backend.core.conf import settings
from backend.core.path_conf import LOCALE_DIR


class I18n:
    """国际化管理器"""

    def __init__(self) -> None:
        self.locales: dict[str, dict[str, Any]] = {}
        self.load_locales()

    @property
    def current_language(self) -> str:
        """获取当前请求的语言"""
        try:
            return ctx.language
        except (AttributeError, LookupError, ContextDoesNotExistError):
            return settings.I18N_DEFAULT_LANGUAGE

    @current_language.setter
    def current_language(self, language: str) -> None:
        """设置当前请求的语言"""
        ctx.language = language

    def load_locales(self) -> None:
        """加载语言文本"""
        patterns = [
            LOCALE_DIR / '*.json',
            LOCALE_DIR / '*.yaml',
            LOCALE_DIR / '*.yml',
        ]

        lang_files = []

        for pattern in patterns:
            lang_files.extend(glob.glob(str(pattern)))

        for lang_file in lang_files:
            with open(lang_file, encoding='utf-8') as f:
                lang = Path(lang_file).stem
                file_type = Path(lang_file).suffix[1:]
                match file_type:
                    case 'json':
                        self.locales[lang] = json.loads(f.read())
                    case 'yaml' | 'yml':
                        self.locales[lang] = yaml.safe_load(f.read())

    def t(self, key: str, default: Any | None = None, **kwargs) -> str:
        """
        翻译函数

        :param key: 目标文本键，支持点分隔，例如 'response.success'
        :param default: 目标语言文本不存在时的默认文本
        :param kwargs: 目标文本中的变量参数
        :return:
        """
        keys = key.split('.')

        # 当前语言包不存在时回退默认语言，保证所有文案都有可读内容
        translation = self.locales.get(self.current_language) or self.locales[settings.I18N_DEFAULT_LANGUAGE]

        for k in keys:
            if isinstance(translation, dict) and k in list(translation.keys()):
                translation = translation[k]
            else:
                # Pydantic 兼容
                translation = None if keys[0] == 'pydantic' else key
                break

        if translation and kwargs:
            translation = translation.format(**kwargs)

        return translation or default


# 创建 i18n 单例
i18n = I18n()

# 创建翻译函数实例
t = i18n.t
