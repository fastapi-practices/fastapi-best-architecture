insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (2049629108257816580, 'code-generator.menu', 'PluginCodeGenerator', '/plugins/code-generator', 10, 'tabler:code', 1, '/plugins/code-generator/views/index', null, 1, 1, 1, '', null, null, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
(2049629108257816581, '新增业务', 'AddGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:add', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816582, '修改业务', 'EditGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:edit', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816583, '删除业务', 'DeleteGenCodeBusiness', null, 0, null, 2, null, 'codegen:business:del', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816584, '新增模型', 'AddGenCodeModel', null, 0, null, 2, null, 'codegen:model:add', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816585, '修改模型', 'EditGenCodeModel', null, 0, null, 2, null, 'codegen:model:edit', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816586, '删除模型', 'DeleteGenCodeModel', null, 0, null, 2, null, 'codegen:model:del', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816587, '导入', 'ImportGenCode', null, 0, null, 2, null, 'codegen:table:import', 1, 0, 1, '', null, 2049629108257816580, now(), null),
(2049629108257816588, '写入', 'WriteGenCode', null, 0, null, 2, null, 'codegen:local:write', 1, 0, 1, '', null, 2049629108257816580, now(), null);

insert into gen_business (id, app_name, table_name, doc_comment, table_comment, class_name, schema_name, filename, datetime_mixin, api_version, gen_path, remark, created_time, updated_time)
values (2112248797819043840, 'test', 'sys_opera_log', '操作日志表', '操作日志表', 'SysOperaLog', 'SysOperaLog', 'sys_opera_log', true, 'v1', null, null, '2025-12-15 15:30:33', null);

insert into gen_column (id, name, comment, type, pd_type, `default`, sort, `length`, is_pk, is_nullable, gen_business_id)
values
(2112248797881958400, 'trace_id', '请求跟踪 ID', 'String', 'str', null, 2, 32, false, false, 2112248797819043840),
(2112248797944872960, 'username', '用户名', 'String', 'str', null, 3, 64, false, true, 2112248797819043840),
(2112248798007787520, 'method', '请求类型', 'String', 'str', null, 4, 32, false, false, 2112248797819043840),
(2112248798070702080, 'title', '操作模块', 'String', 'str', null, 5, 256, false, false, 2112248797819043840),
(2112248798133616640, 'path', '请求路径', 'String', 'str', null, 6, 512, false, false, 2112248797819043840),
(2112248798196531200, 'ip', 'IP地址', 'String', 'str', null, 7, 64, false, false, 2112248797819043840),
(2112248798259445760, 'country', '国家', 'String', 'str', null, 8, 64, false, true, 2112248797819043840),
(2112248798322360320, 'region', '地区', 'String', 'str', null, 9, 64, false, true, 2112248797819043840),
(2112248798385274880, 'city', '城市', 'String', 'str', null, 10, 64, false, true, 2112248797819043840),
(2112248798448189440, 'user_agent', '请求头', 'String', 'str', null, 11, 512, false, false, 2112248797819043840),
(2112248798511104000, 'os', '操作系统', 'String', 'str', null, 12, 64, false, true, 2112248797819043840),
(2112248798574018560, 'browser', '浏览器', 'String', 'str', null, 13, 64, false, true, 2112248797819043840),
(2112248798636933120, 'device', '设备', 'String', 'str', null, 14, 64, false, true, 2112248797819043840),
(2112248798699847680, 'args', '请求参数', 'JSON', 'dict', null, 15, 0, false, true, 2112248797819043840),
(2112248798762762240, 'status', '操作状态（0异常 1正常）', 'INTEGER', 'int', null, 16, 0, false, false, 2112248797819043840),
(2112248798825676800, 'code', '操作状态码', 'String', 'str', null, 17, 32, false, false, 2112248797819043840),
(2112248798888591360, 'msg', '提示消息', 'TEXT', 'str', null, 18, 0, false, true, 2112248797819043840),
(2112248798951505920, 'cost_time', '请求耗时（ms）', 'String', 'str', null, 19, 0, false, false, 2112248797819043840),
(2112248799014420480, 'opera_time', '操作时间', 'String', 'str', null, 20, 0, false, false, 2112248797819043840);
