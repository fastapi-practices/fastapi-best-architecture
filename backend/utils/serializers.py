from collections import defaultdict, namedtuple
from collections.abc import Sequence
from decimal import Decimal
from typing import Any, TypeAlias, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

from backend.common.log import log

RowData: TypeAlias = Row[Any] | RowMapping | Any

R = TypeVar('R', bound=RowData)


class MsgSpecJSONResponse(JSONResponse):
    """
    使用高性能的 msgspec 库将数据序列化为 JSON 的响应类
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)


def select_columns_serialize(row: R) -> dict[str, Any]:
    """
    序列化 SQLAlchemy 查询表的列，不包含关联列

    :param row: SQLAlchemy 查询结果行
    :return:
    """
    result = {}
    for column in row.__table__.columns.keys():
        value = getattr(row, column)
        if isinstance(value, Decimal):
            value = decimal_encoder(value)
        result[column] = value
    return result


def select_list_serialize(row: Sequence[R]) -> list[dict[str, Any]]:
    """
    序列化 SQLAlchemy 查询列表

    :param row: SQLAlchemy 查询结果列表
    :return:
    """
    return [select_columns_serialize(item) for item in row]


def select_as_dict(row: R, *, use_alias: bool = False) -> dict[str, Any]:
    """
    将 SQLAlchemy 查询结果转换为字典，可以包含关联数据

    :param row: SQLAlchemy 查询结果行
    :param use_alias: 是否使用别名作为列名
    :return:
    """
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        result = {}
        mapper = class_mapper(row.__class__)  # type: ignore
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)

    return result


def select_join_serialize(  # noqa: C901
    row: R | Sequence[R],
    relationships: list[str] | None = None,
    *,
    return_as_dict: bool = False,
) -> dict[str, Any] | list[dict[str, Any]] | tuple[Any, ...] | list[tuple[Any, ...]] | None:
    """
    将 SQLAlchemy 连接查询结果序列化为字典或 namedtuple

    扁平序列化（relationships=None）：
        所有结果平铺到同一层级，不嵌套
        例：Result(name='Alice', dept=Dept(...))

    嵌套序列化：
        根据关系类型嵌套组织数据，支持层级结构
        例：relationships=['User-m2o-Dept', 'User-m2m-Role:permissions']
        输出：Result(name='Alice', dept=Dept(...), permissions=[Role(...)])

    关系格式：source_model-type-target_model[:custom_name]
        - type: o2m(一对多), m2o(多对一), o2o(一对一), m2m(多对多)
        - o2m/m2m: 目标字段名自动加 's' 复数化
        - m2o/o2o: 目标字段名保持单数
        - custom_name: 自定义目标字段名

    :param row: SQLAlchemy 查询结果
    :param relationships: 关系定义列表
    :param return_as_dict: True 返回字典，False 返回 namedtuple
    :return:
    """
    list_relationship_types = {'o2m', 'm2m'}
    all_relationship_types = {'o2m', 'm2o', 'o2o', 'm2m'}

    def get_obj_id(target_obj: Any) -> int | str:
        return getattr(target_obj, 'id', None) or id(target_obj)

    def extract_row_elements(row_data: Any) -> tuple:
        return row_data if hasattr(row_data, '__getitem__') else (row_data,)

    def get_relationship_key(model: str, relationship_type: str, custom_field: str | None) -> str:
        return custom_field or (model if relationship_type not in list_relationship_types else f'{model}s')

    def parse_relationships(relationship_list: list[str]) -> tuple[dict, dict, dict]:
        if not relationship_list:
            return {}, {}, {}

        graph = defaultdict(dict)
        reverse = {}
        customs = {}

        for rel_str in relationship_list:
            parts = rel_str.split(':', 1)
            rel_part = parts[0].strip()
            custom_name = parts[1].strip() if len(parts) > 1 else None

            info = rel_part.split('-')
            if len(info) != 3:
                log.warning(f'Invalid relationship: "{rel_str}", expected "source-type-target[:custom]"')
                continue

            src, parsed_type, dst = (x.lower() for x in info)
            if parsed_type not in all_relationship_types:
                log.warning(
                    f'Invalid relationship type: "{parsed_type}" in "{rel_str}", '
                    f'must be one of: {", ".join(all_relationship_types)}'
                )
                continue

            graph[src][dst] = parsed_type
            reverse[dst] = src
            if custom_name:
                customs[src, dst] = custom_name

        return graph, reverse, customs

    def get_model_columns(model_obj: Any) -> list[str]:
        mapper = class_mapper(type(model_obj))
        return [
            prop.key
            for prop in mapper.iterate_properties
            if isinstance(prop, (ColumnProperty, SynonymProperty)) and hasattr(model_obj, prop.key)
        ]

    def dedupe_objects(obj_list: list[Any]) -> list[Any]:
        seen = set()
        unique = []
        for item in obj_list:
            item_id = getattr(item, 'id', None)
            if item_id is not None and item_id not in seen:
                seen.add(item_id)
                unique.append(item)
        return unique

    def build_namedtuple(name: str, data: dict) -> Any:
        if return_as_dict or name not in namedtuple_cache:
            return None
        for field in namedtuple_cache[name]._fields:
            if field not in data:
                data[field] = None
        return namedtuple_cache[name](**data)

    # 输入验证
    if not row:
        return None

    rows_list = [row] if not isinstance(row, list) else row
    if not rows_list:
        return None

    # 主对象信息
    first_row = extract_row_elements(rows_list[0])
    primary_obj = first_row[0]
    if primary_obj is None:
        return None

    primary_obj_name = type(primary_obj).__name__.lower()
    primary_columns = get_model_columns(primary_obj)

    # 关系解析
    relation_graph, reverse_relation, custom_names = parse_relationships(relationships or [])
    has_relationships = bool(relation_graph)

    # 预处理模型信息
    model_info = {}
    cls_idx = {}

    for row_item in rows_list:
        row_elements = extract_row_elements(row_item)
        for idx, element in enumerate(row_elements):
            if element is None:
                continue
            element_cls = type(element).__name__.lower()
            if element_cls not in model_info:
                model_info[element_cls] = get_model_columns(element)
            if element_cls not in cls_idx:
                cls_idx[element_cls] = idx

    # 数据分组
    main_objects = {}
    children_objects = defaultdict(lambda: defaultdict(list))

    for row_item in rows_list:
        row_elements = extract_row_elements(row_item)
        if not row_elements or row_elements[0] is None:
            continue

        main_obj = row_elements[0]
        main_id = get_obj_id(main_obj)

        if main_id not in main_objects:
            main_objects[main_id] = main_obj

        for child_obj in row_elements[1:]:
            if child_obj is None:
                continue
            child_type = type(child_obj).__name__.lower()
            children_objects[main_id][child_type].append(child_obj)

    if not main_objects:
        return None

    # namedtuple 类型预生成
    namedtuple_cache = {}
    if not return_as_dict:
        for model_name, model_columns in model_info.items():
            if not model_columns:
                continue

            field_list = model_columns.copy()
            if has_relationships:
                for target, target_rtype in relation_graph.get(model_name, {}).items():
                    nt_key = get_relationship_key(target, target_rtype, custom_names.get((model_name, target)))
                    field_list.append(nt_key)
                field_list = list(dict.fromkeys(field_list))

            namedtuple_cache[model_name] = namedtuple(model_name.capitalize(), field_list)  # noqa: PYI024

    # 嵌套关系层级结构（一次性构建）
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    if has_relationships:
        for row_item in rows_list:
            row_elements = extract_row_elements(row_item)
            if not row_elements or row_elements[0] is None:
                continue

            main_id = get_obj_id(row_elements[0])
            m_type_name = type(row_elements[0]).__name__.lower()

            for idx, rel_obj in enumerate(row_elements[1:], 1):  # noqa: B007
                if rel_obj is None:
                    continue

                rel_type_name = type(rel_obj).__name__.lower()

                if rel_type_name in reverse_relation:
                    parent_type = reverse_relation[rel_type_name]
                    parent_idx = cls_idx.get(parent_type)
                    parent = (
                        row_elements[parent_idx] if parent_idx is not None and parent_idx < len(row_elements) else None
                    )
                elif rel_type_name in relation_graph.get(m_type_name, {}):
                    parent = row_elements[0]
                else:
                    continue

                if parent is None:
                    continue

                parent_pk = getattr(parent, 'id', None)
                if parent_pk is not None:
                    hierarchy[main_id][rel_type_name][parent_pk].append(rel_obj)

    # 结果构建函数
    def build_flat(target_id: int, target_obj: Any) -> dict[str, Any]:
        result = {col: getattr(target_obj, col, None) for col in primary_columns}

        for cls_type in children_objects[target_id]:
            if cls_type == primary_obj_name:
                continue

            unique_children = dedupe_objects(children_objects[target_id][cls_type])
            child_columns = model_info.get(cls_type, [])

            count = len(unique_children)
            field_key = cls_type if count <= 1 else f'{cls_type}s'

            if count == 0:
                result[field_key] = []
            elif count == 1:
                obj_data = {col: getattr(unique_children[0], col, None) for col in child_columns}
                result[field_key] = obj_data if return_as_dict else build_namedtuple(cls_type, obj_data)
            else:
                if return_as_dict:
                    result[field_key] = [{col: getattr(c, col, None) for col in child_columns} for c in unique_children]
                else:
                    result[field_key] = [
                        build_namedtuple(cls_type, {col: getattr(c, col, None) for col in child_columns})
                        for c in unique_children
                    ]

        return result

    def build_nested(target_id: int, target_obj: Any) -> dict[str, Any]:
        result = {col: getattr(target_obj, col, None) for col in primary_columns}
        current_hierarchy = hierarchy.get(target_id, defaultdict(lambda: defaultdict(list)))

        def recursive_build(cls_name: str, pk: int) -> list:
            nested_dict = current_hierarchy.get(cls_name)
            if nested_dict is None:
                return []
            objs = dedupe_objects(nested_dict.get(pk, []))
            if not objs:
                return []

            output = []
            for item in objs:
                item_data = {col: getattr(item, col, None) for col in model_info[cls_name]}

                for sub_type, sub_rel_type in relation_graph.get(cls_name, {}).items():
                    sub_pk = getattr(item, 'id', None)
                    if sub_pk is None:
                        continue

                    sub_list = recursive_build(sub_type, sub_pk)
                    sub_key = get_relationship_key(sub_type, sub_rel_type, custom_names.get((cls_name, sub_type)))

                    if sub_rel_type not in list_relationship_types:
                        item_data[sub_key] = sub_list[0] if sub_list else None
                    else:
                        item_data[sub_key] = sub_list

                output.append(item_data if return_as_dict else build_namedtuple(cls_name, item_data))

            return output

        for top_type, top_rtype in relation_graph.get(primary_obj_name, {}).items():
            instances = recursive_build(top_type, target_id)
            top_key = get_relationship_key(top_type, top_rtype, custom_names.get((primary_obj_name, top_type)))

            if top_rtype not in list_relationship_types:
                result[top_key] = instances[0] if instances else None
            else:
                result[top_key] = instances

        return result

    # 最终结果构建
    final_results = []
    processed_ids = set()

    for row_item in rows_list:
        row_elements = extract_row_elements(row_item)
        if not row_elements or row_elements[0] is None:
            continue

        main_obj = row_elements[0]
        main_id = get_obj_id(main_obj)

        if main_id not in main_objects or main_id in processed_ids:
            continue

        processed_ids.add(main_id)

        result_data = build_nested(main_id, main_obj) if has_relationships else build_flat(main_id, main_obj)

        if not return_as_dict:
            result_type = namedtuple('Result', result_data.keys())  # noqa: PYI024
            final_results.append(result_type(**result_data))
        else:
            final_results.append(result_data)

    return final_results[0] if len(final_results) == 1 else final_results
