import os
import subprocess
import sys
import warnings

from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any

from pydantic import GetCoreSchemaHandler, HttpUrl, PlainSerializer, computed_field, field_serializer
from pydantic_core import core_schema
from typing_extensions import TypeAliasType

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase
from backend.utils.timezone import timezone


class _SerializationSchema(SchemaBase):
    happened_at: datetime
    optional_value: str | None = None
    status: StatusType
    steps: list[int]


class _ContainerSchema(SchemaBase):
    typed_values: list[datetime]
    typed_mapping: dict[str, datetime]
    any_value: Any
    optional_any: Any | None
    any_mapping: dict[str, Any]


class _SpecializedSerializerSchema(SchemaBase):
    payload: bytes

    @field_serializer('payload', when_used='json')
    def serialize_payload(self, value: bytes) -> str:
        return value.decode()


SerializedUrl = Annotated[HttpUrl, PlainSerializer(lambda value: str(value), return_type=str)]


class _PlainSerializerSchema(SchemaBase):
    homepage: SerializedUrl


class _WrappedDatetime:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            lambda value: value,
            core_schema.datetime_schema(),
            serialization=core_schema.wrap_serializer_function_ser_schema(
                lambda value, next_handler: f'wrapped<{next_handler(value)}>',
                when_used='json',
            ),
        )


class _DateLike:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            lambda value: value,
            core_schema.datetime_schema(),
        )


class _CustomCoreSerializerSchema(SchemaBase):
    happened_at: _WrappedDatetime
    date_like: _DateLike


DatetimeAlias = TypeAliasType('DatetimeAlias', datetime)


class _AliasAndComputedSchema(SchemaBase):
    happened_at: DatetimeAlias

    @computed_field
    @property
    def computed_at(self) -> datetime:
        return self.happened_at


class _NestedSchema(SchemaBase):
    visible: str
    hidden: str


class _NestedChildSchema(_NestedSchema):
    child_only: str


class _NestedContainerSchema(SchemaBase):
    nested: _NestedSchema


def test_schema_base_import_has_no_deprecated_json_encoder_warning() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env['PYTHONPATH'] = str(repo_root)
    script = (
        'import warnings; '
        'from pydantic.warnings import PydanticDeprecatedSince20; '
        'warnings.simplefilter("error", PydanticDeprecatedSince20); '
        'from backend.common.schema import SchemaBase'
    )

    result = subprocess.run(
        [sys.executable, '-c', script],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_schema_base_preserves_field_filters_and_datetime_format() -> None:
    happened_at = datetime(2026, 7, 13, 8, 30, tzinfo=UTC)
    schema = _SerializationSchema(happened_at=happened_at, status=1, steps=[1])
    serialized_time = timezone.to_str(timezone.from_datetime(happened_at))

    assert schema.model_dump(exclude={'steps'}) == {
        'happened_at': happened_at,
        'optional_value': None,
        'status': 1,
    }
    assert schema.model_dump(mode='json', include={'happened_at'}) == {
        'happened_at': serialized_time,
    }
    assert schema.model_dump(mode='json', exclude={'steps'}, exclude_none=True) == {
        'happened_at': serialized_time,
        'status': 1,
    }


def test_schema_base_preserves_typed_and_any_container_datetime_formats() -> None:
    happened_at = datetime(2026, 7, 13, 8, 30, tzinfo=UTC)
    schema = _ContainerSchema(
        typed_values=[happened_at],
        typed_mapping={'happened_at': happened_at},
        any_value=happened_at,
        optional_any=happened_at,
        any_mapping={'happened_at': happened_at},
    )
    serialized_time = timezone.to_str(timezone.from_datetime(happened_at))

    assert schema.model_dump(mode='json') == {
        'typed_values': [serialized_time],
        'typed_mapping': {'happened_at': serialized_time},
        'any_value': serialized_time,
        'optional_any': serialized_time,
        'any_mapping': {'happened_at': '2026-07-13T08:30:00Z'},
    }


def test_schema_base_preserves_nested_filters_and_declared_type_boundary() -> None:
    filtered = _NestedContainerSchema(
        nested=_NestedSchema(visible='yes', hidden='no'),
    )
    child = _NestedContainerSchema(
        nested=_NestedChildSchema(visible='yes', hidden='no', child_only='private'),
    )
    include = {'nested': {'visible'}}
    exclude = {'nested': {'hidden'}}

    assert filtered.model_dump(include=include) == {'nested': {'visible': 'yes'}}
    assert filtered.model_dump(mode='json', exclude=exclude) == {'nested': {'visible': 'yes'}}
    assert child.model_dump() == {'nested': {'visible': 'yes', 'hidden': 'no'}}
    assert child.model_dump(mode='json') == {'nested': {'visible': 'yes', 'hidden': 'no'}}


def test_schema_base_preserves_serialization_json_schema() -> None:
    schema = _SerializationSchema.model_json_schema(mode='serialization')
    properties = schema['properties']

    assert properties['happened_at']['type'] == 'string'
    assert properties['happened_at']['format'] == 'date-time'
    assert properties['status']['$ref'].startswith('#/$defs/')
    assert properties['steps']['type'] == 'array'
    assert properties['steps']['items']['type'] == 'integer'


def test_schema_base_serializes_enum_without_warning() -> None:
    schema = _SerializationSchema(
        happened_at=datetime(2026, 7, 13, 8, 30, tzinfo=UTC),
        status=1,
        steps=[],
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        assert schema.model_dump()['status'] == 1
        assert schema.model_dump(mode='json')['status'] == 1

    assert caught == []


def test_schema_base_allows_specialized_serializers_without_warning() -> None:
    decorated = _SpecializedSerializerSchema(payload=b'ok')
    annotated = _PlainSerializerSchema(homepage='https://example.com')

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        assert decorated.model_dump(mode='json') == {'payload': 'ok'}
        assert annotated.model_dump(mode='json') == {'homepage': 'https://example.com/'}

    assert caught == []


def test_schema_base_does_not_change_custom_core_serializer_handler() -> None:
    happened_at = datetime(2026, 7, 13, 8, 30, tzinfo=UTC)
    schema = _CustomCoreSerializerSchema(happened_at=happened_at, date_like=happened_at)

    assert schema.model_dump(mode='json') == {
        'happened_at': 'wrapped<2026-07-13T08:30:00Z>',
        'date_like': '2026-07-13T08:30:00Z',
    }


def test_schema_base_serializes_datetime_alias_and_computed_field() -> None:
    happened_at = datetime(2026, 7, 13, 8, 30, tzinfo=UTC)
    schema = _AliasAndComputedSchema(happened_at=happened_at)
    serialized_time = timezone.to_str(timezone.from_datetime(happened_at))

    assert schema.model_dump(mode='json') == {
        'happened_at': serialized_time,
        'computed_at': serialized_time,
    }


def test_schema_base_preserves_snowflake_id_serializer() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env['DATABASE_PK_MODE'] = 'snowflake'
    env['PYTHONPATH'] = str(repo_root)
    script = (
        'from pydantic import ConfigDict; '
        'from backend.common.schema import SchemaBase; '
        'SnowflakeSchema = type('
        '"SnowflakeSchema", '
        '(SchemaBase,), '
        '{"__annotations__": {"id": int}, "model_config": ConfigDict(from_attributes=True)}'
        '); '
        'assert SnowflakeSchema(id=9007199254740993).model_dump(mode="json") '
        '== {"id": "9007199254740993"}'
    )

    result = subprocess.run(
        [sys.executable, '-c', script],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
