from datetime import datetime
from types import UnionType
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    GetCoreSchemaHandler,
    SerializerFunctionWrapHandler,
    validate_email,
)
from pydantic_core import PydanticUndefined, core_schema
from typing_extensions import TypeAliasType

from backend.common.enums import PrimaryKeyType
from backend.core.conf import settings
from backend.utils.timezone import timezone

CustomPhoneNumber = Annotated[str, Field(pattern=r'^1[3-9]\d{9}$')]


def _serialize_datetime(value: datetime) -> str:
    if value.tzinfo is not None and value.tzinfo != timezone.tz_info:
        return timezone.to_str(timezone.from_datetime(value))
    return timezone.to_str(value)


def _serialize_any_datetime(value: Any, handler: SerializerFunctionWrapHandler) -> Any:
    if isinstance(value, datetime):
        return _serialize_datetime(value)
    return handler(value)


def _contains_datetime(annotation: Any) -> bool:
    if isinstance(annotation, TypeAliasType):
        return _contains_datetime(annotation.__value__)
    if isinstance(annotation, type) and issubclass(annotation, datetime):
        return True
    return any(_contains_datetime(arg) for arg in get_args(annotation))


def _unwrap_annotated(annotation: Any) -> Any:
    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


def _is_any_field(annotation: Any) -> bool:
    annotation = _unwrap_annotated(annotation)
    if isinstance(annotation, TypeAliasType):
        return _is_any_field(annotation.__value__)
    if annotation is Any:
        return True
    if get_origin(annotation) in (Union, UnionType):
        return any(_is_any_field(arg) for arg in get_args(annotation) if arg is not type(None))
    return False


def _set_datetime_serializer(schema: Any, handler: GetCoreSchemaHandler) -> None:
    if isinstance(schema, dict):
        if 'serialization' in schema:
            return
        if schema.get('type') == 'definition-ref':
            _set_datetime_serializer(handler.resolve_ref_schema(schema), handler)
            return
        if schema.get('type') == 'datetime' and 'serialization' not in schema:
            schema['serialization'] = core_schema.plain_serializer_function_ser_schema(
                _serialize_datetime,
                when_used='json',
            )
        for value in schema.values():
            _set_datetime_serializer(value, handler)
    elif isinstance(schema, list):
        for value in schema:
            _set_datetime_serializer(value, handler)


def _find_model_fields_schema(schema: Any, model_name: str) -> dict[str, Any]:
    if isinstance(schema, dict):
        if schema.get('type') == 'model-fields' and schema.get('model_name') == model_name:
            return schema
        for value in schema.values():
            if fields := _find_model_fields_schema(value, model_name):
                return fields
    elif isinstance(schema, list):
        for value in schema:
            if fields := _find_model_fields_schema(value, model_name):
                return fields
    return {}


def _set_annotation_datetime_serializer(
    schema: Any,
    annotation: Any,
    handler: GetCoreSchemaHandler,
) -> None:
    if _is_any_field(annotation):
        if 'serialization' not in schema:
            schema['serialization'] = core_schema.wrap_serializer_function_ser_schema(
                _serialize_any_datetime,
                when_used='json',
            )
    elif _contains_datetime(annotation):
        _set_datetime_serializer(schema, handler)


def _get_computed_return_annotation(field_info: Any) -> Any:
    wrapped_property = field_info.wrapped_property
    function = getattr(wrapped_property, 'fget', None) or getattr(wrapped_property, 'func', None)
    if function is not None:
        try:
            return get_type_hints(function).get('return', field_info.return_type)
        except (NameError, TypeError):
            pass
    return field_info.return_type


def _set_model_datetime_serializers(
    schema: core_schema.CoreSchema,
    model: type[BaseModel],
    handler: GetCoreSchemaHandler,
) -> None:
    model_fields_schema = _find_model_fields_schema(schema, model.__name__)
    field_schemas = model_fields_schema.get('fields', {})
    for field_name, field_info in model.__pydantic_fields__.items():
        if field_schema := field_schemas.get(field_name, {}).get('schema'):
            _set_annotation_datetime_serializer(field_schema, field_info.annotation, handler)

    computed_schemas = {
        field['property_name']: field['return_schema'] for field in model_fields_schema.get('computed_fields', [])
    }
    for field_name, field_info in model.__pydantic_computed_fields__.items():
        if field_schema := computed_schemas.get(field_name):
            annotation = _get_computed_return_annotation(field_info)
            if annotation is not PydanticUndefined:
                _set_annotation_datetime_serializer(field_schema, annotation, handler)


class CustomEmailStr(EmailStr):
    """自定义邮箱类型"""

    @classmethod
    def _validate(cls, input_value: str, /) -> str | None:
        return None if not input_value else validate_email(input_value)[1]


class SchemaBase(BaseModel):
    """基础模型配置"""

    model_config = ConfigDict(
        use_enum_values=True,
    )

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        schema = handler(source_type)
        _set_model_datetime_serializers(schema, source_type, handler)
        return schema

    if PrimaryKeyType.snowflake == settings.DATABASE_PK_MODE:
        from pydantic import field_serializer

        # 详情：https://fastapi-practices.github.io/fastapi_best_architecture_docs/backend/reference/pk.html#%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9
        @field_serializer('id', check_fields=False)
        def serialize_id(self, value: int) -> str | int:
            if self.model_config.get('from_attributes'):
                return str(value)
            return value


def ser_string(value: Any) -> str | None:
    if value:
        return str(value)
    return value
