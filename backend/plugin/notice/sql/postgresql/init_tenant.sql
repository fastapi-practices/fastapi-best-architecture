do $$
declare
    notice_menu_id bigint;
begin
    insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    values ('notice.menu', 'PluginNotice', '/plugins/notice', 9, 'fe:notice-push', 1, '/plugins/notice/views/index', null, 1, 1, 1, '', null, (select id from sys_menu where name = 'System'), now(), null)
    returning id into notice_menu_id;

    insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    values
    ('新增', 'AddNotice', null, 0, null, 2, null, 'sys:notice:add', 1, 0, 1, '', null, notice_menu_id, now(), null),
    ('修改', 'EditNotice', null, 0, null, 2, null, 'sys:notice:edit', 1, 0, 1, '', null, notice_menu_id, now(), null),
    ('删除', 'DeleteNotice', null, 0, null, 2, null, 'sys:notice:del', 1, 0, 1, '', null, notice_menu_id, now(), null);
end $$;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;

insert into sys_notice (id, title, type, status, content, created_time, updated_time, tenant_id)
values (1, 'hahahahahaahahaha', 0, 1, '你好😄

```
print(''fba yyds'')
```

⚡⚡⚡

| col1 | col2 | col3 |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |

* 1
* 2
* 3
', '2025-12-15 15:33:16', null, 0);

select setval(pg_get_serial_sequence('sys_notice', 'id'),coalesce(max(id), 0) + 1, true) from sys_notice;
