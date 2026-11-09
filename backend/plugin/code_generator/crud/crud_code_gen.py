from collections.abc import Sequence

from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCodeGen:
    """代码生成 CRUD 类"""

    @staticmethod
    async def get_all_tables(db: AsyncSession, table_schema: str) -> Sequence[RowMapping]:
        """
        获取所有表名

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :return:
        """
        sql = """
        select
          c.relname as table_name,
          obj_description (c.oid) as table_comment
        from
          pg_class c
          left join pg_namespace n on n.oid = c.relnamespace
        where
          c.relkind = 'r'
          and c.relname not like 'gen_%'
          and n.nspname = :table_schema;
        """
        stmt = text(sql).bindparams(table_schema='public')
        result = await db.execute(stmt)
        return result.mappings().all()

    @staticmethod
    async def get_table(db: AsyncSession, table_schema: str, table_name: str) -> RowMapping | None:
        """
        获取表信息

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :param table_name: 表名
        :return:
        """
        sql = """
        select
          c.relname as table_name,
          obj_description (c.oid) as table_comment
        from
          pg_class c
          left join pg_namespace n on n.oid = c.relnamespace
        where
          c.relkind = 'r'
          and c.relname not like 'gen_%'
          and c.relname = :table_name
          and n.nspname = :table_schema;
        """
        stmt = text(sql).bindparams(table_schema='public', table_name=table_name)
        result = await db.execute(stmt)
        row = result.fetchone()
        return row._mapping if row else None

    @staticmethod
    async def get_all_columns(db: AsyncSession, table_schema: str, table_name: str) -> Sequence[RowMapping]:
        """
        获取所有列信息

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :param table_name: 表名
        :return:
        """
        sql = """
        select
          a.attname as column_name,
          case
            when exists (
                select
                  1
                from
                  pg_constraint c
                where
                  c.conrelid = t.oid
                  and c.contype = 'p'
                  and a.attnum = any (c.conkey)
              ) then
              1
            else
              0
          end as is_pk,
          case
            when a.attnotnull
              or exists (
                select
                  1
                from
                  pg_constraint c
                where
                  c.conrelid = t.oid
                  and c.contype = 'p'
                  and a.attnum = any (c.conkey)
              ) then
              0
            else
              1
          end as is_nullable,
          a.attnum as sort,
          col_description (t.oid, a.attnum) as column_comment,
          pg_catalog.format_type (a.atttypid, a.atttypmod) as column_type
        from
          pg_attribute a
          join pg_class t on a.attrelid = t.
          oid join pg_namespace n on n.oid = t.relnamespace
        where
          a.attnum > 0
          and not a.attisdropped
          and a.attname <> 'id'
          and a.attname <> 'created_time'
          and a.attname <> 'updated_time'
          and a.attname <> 'deleted'
          and a.attname <> 'deleted_time'
          and t.relname = :table_name
          and n.nspname = :table_schema
        order by
          sort;
        """
        stmt = text(sql).bindparams(table_schema='public', table_name=table_name)
        result = await db.execute(stmt)
        return result.mappings().all()


code_gen_dao: CRUDCodeGen = CRUDCodeGen()
