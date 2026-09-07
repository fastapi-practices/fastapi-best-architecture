delete from sys_menu where name in ('AddGenCodeBusiness', 'EditGenCodeBusiness', 'DeleteGenCodeBusiness', 'AddGenCodeModel', 'EditGenCodeModel', 'DeleteGenCodeModel', 'ImportGenCode', 'WriteGenCode');

delete from sys_menu where name = 'PluginCodeGenerator';

drop table if exists code_gen_column;
drop table if exists code_gen_business;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
