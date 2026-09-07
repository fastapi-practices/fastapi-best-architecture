delete from sys_menu where name in ('AddGenCodeBusiness', 'EditGenCodeBusiness', 'DeleteGenCodeBusiness', 'AddGenCodeModel', 'EditGenCodeModel', 'DeleteGenCodeModel', 'ImportGenCode', 'WriteGenCode');

delete from sys_menu where name = 'PluginCodeGenerator';

drop table if exists code_gen_column;
drop table if exists code_gen_business;
