<a id="v1.14.0"></a>
# [v1.14.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.14.0) - 2026-05-30

## What's Changed
* Update changelog for v1.13.4 by [@wu-clan](https://github.com/wu-clan) in [#1170](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1170)
* Update xdb dependency and database file by [@wu-clan](https://github.com/wu-clan) in [#1171](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1171)
* Optimize database operations within loops by [@wu-clan](https://github.com/wu-clan) in [#1177](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1177)
* Optimize some global variable definitions by [@wu-clan](https://github.com/wu-clan) in [#1178](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1178)
* Optimize SQL script execution in the CLI by [@wu-clan](https://github.com/wu-clan) in [#1181](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1181)
* Fix cache invalidation decorator usage by [@wu-clan](https://github.com/wu-clan) in [#1182](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1182)
* Optimize user session logging and deletion by [@wu-clan](https://github.com/wu-clan) in [#1185](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1185)
* Optimize operation log truncation handling by [@wu-clan](https://github.com/wu-clan) in [#1186](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1186)
* Add opera log task cancel to lifespan by [@wu-clan](https://github.com/wu-clan) in [#1187](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1187)
* Optimize Grafana observability metrics and config by [@wu-clan](https://github.com/wu-clan) in [#1188](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1188)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [#1189](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1189)
* Optimize the usage of setex for redis by [@wu-clan](https://github.com/wu-clan) in [#1190](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1190)
* Refactor physical deletion to logical deletion by [@wu-clan](https://github.com/wu-clan) in [#1191](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1191)
* Fix task scheduler unpack fields by [@wu-clan](https://github.com/wu-clan) in [#1192](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1192)
* Update the version number to 1.14.0 by [@wu-clan](https://github.com/wu-clan) in [#1193](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1193)


**Full Changelog**: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.4...v1.14.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.14.0]


<a id="v1.13.4"></a>
# [v1.13.4](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.13.4) - 2026-04-28

## What's Changed
* Update changelog for v1.13.3 by [@wu-clan](https://github.com/wu-clan) in [#1149](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1149)
* Update the architecture description in README by [@wu-clan](https://github.com/wu-clan) in [#1150](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1150)
* Fix app pytest client fixture scope by [@IAseven](https://github.com/IAseven) in [#1152](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1152)
* Remove cleanup operations after plugin install by [@wu-clan](https://github.com/wu-clan) in [#1154](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1154)
* Fix mysql enum data type mismatch by [@wu-clan](https://github.com/wu-clan) in [#1155](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1155)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [#1156](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1156)
* Add plugin depends on and lifecycle ordering by [@AH-Toby](https://github.com/AH-Toby) in [#1153](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1153)
* Update plugin README content format by [@wu-clan](https://github.com/wu-clan) in [#1158](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1158)
* Update Grafana dashboard and datasource config by [@wu-clan](https://github.com/wu-clan) in [#1159](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1159)
* Add database and queue observability by [@wu-clan](https://github.com/wu-clan) in [#1160](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1160)
* Fix Grafana tempo and observability config by [@wu-clan](https://github.com/wu-clan) in [#1161](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1161)
* Add the snowflake ID enabled config by [@wu-clan](https://github.com/wu-clan) in [#1162](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1162)
* Fix the add plugin CLI command config by [@wu-clan](https://github.com/wu-clan) in [#1163](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1163)
* Optimize the core code ordering of plugins by [@wu-clan](https://github.com/wu-clan) in [#1164](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1164)
* Add uninstall plugin operation checks by [@wu-clan](https://github.com/wu-clan) in [#1165](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1165)
* Fix multi level cache storage logic by [@wu-clan](https://github.com/wu-clan) in [#1166](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1166)
* Fix typing warnings for return methods by [@wu-clan](https://github.com/wu-clan) in [#1167](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1167)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [#1168](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1168)
* Update the version number to 1.13.4 by [@wu-clan](https://github.com/wu-clan) in [#1169](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1169)

## New Contributors
* [@AH-Toby](https://github.com/AH-Toby) made their first contribution in [#1153](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1153)

**Full Changelog**: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.3...v1.13.4

## Contributors

<a href="https://github.com/AH-Toby"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FAH-Toby.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@AH-Toby"></a>
<a href="https://github.com/IAseven"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FIAseven.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@IAseven"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.13.4]


<a id="v1.13.3"></a>
# [v1.13.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.13.3) - 2026-04-08

## What's Changed
* Update changelog for v1.13.2 by [@wu-clan](https://github.com/wu-clan) in [#1124](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1124)
* Fix the logic related to the status field by [@wu-clan](https://github.com/wu-clan) in [#1125](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1125)
* Fix code generation menu sql scripts by [@wu-clan](https://github.com/wu-clan) in [#1127](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1127)
* Update plugins and monitoring permissions by [@wu-clan](https://github.com/wu-clan) in [#1126](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1126)
* Add custom cursor pagination support by [@wu-clan](https://github.com/wu-clan) in [#1128](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1128)
* Update the plugin requirements check by [@wu-clan](https://github.com/wu-clan) in [#1129](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1129)
* Update plugin config and dependency cache by [@wu-clan](https://github.com/wu-clan) in [#1130](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1130)
* Fix plugin dependencies for redis instance by [@wu-clan](https://github.com/wu-clan) in [#1133](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1133)
* Fix current superuser permission validation by [@wu-clan](https://github.com/wu-clan) in [#1138](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1138)
* Fix the return of registered task results by [@wu-clan](https://github.com/wu-clan) in [#1139](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1139)
* Refactor plugin dependency cache and check by [@wu-clan](https://github.com/wu-clan) in [#1140](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1140)
* Add the installation frontend plugin CLI by [@wu-clan](https://github.com/wu-clan) in [#1141](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1141)
* Update custom reload filter call rules by [@wu-clan](https://github.com/wu-clan) in [#1144](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1144)
* Fix custom email model return type by [@wu-clan](https://github.com/wu-clan) in [#1145](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1145)
* Add superpowers to gitignore file by [@wu-clan](https://github.com/wu-clan) in [#1146](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1146)
* Add plugin system hook function mechanism by [@yuWorm](https://github.com/yuWorm) in [#1142](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1142)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [#1147](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1147)
* Update the version number to 1.13.3 by [@wu-clan](https://github.com/wu-clan) in [#1148](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1148)

## New Contributors
* [@yuWorm](https://github.com/yuWorm) made their first contribution in [#1142](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1142)

**Full Changelog**: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.2...v1.13.3

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>
<a href="https://github.com/yuWorm"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FyuWorm.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@yuWorm"></a>

[Changes][v1.13.3]


<a id="v1.13.2"></a>
# [v1.13.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.13.2) - 2026-03-23

## What's Changed
* Update changelog for v1.13.1 by [@wu-clan](https://github.com/wu-clan) in [#1103](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1103)
* Fix log type check and default formatter by [@wu-clan](https://github.com/wu-clan) in [#1104](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1104)
* Replace the uvicorn runner with granian by [@wu-clan](https://github.com/wu-clan) in [#1105](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1105)
* Update user id context setting location by [@wu-clan](https://github.com/wu-clan) in [#1110](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1110)
* Update refresh token geo-checksum response by [@wu-clan](https://github.com/wu-clan) in [#1111](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1111)
* Update plugin dynamic import check by [@wu-clan](https://github.com/wu-clan) in [#1112](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1112)
* Fix rbac permission checking logic by [@wu-clan](https://github.com/wu-clan) in [#1113](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1113)
* Fix user menu permission code update by [@wu-clan](https://github.com/wu-clan) in [#1114](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1114)
* Fix typos in code and comments by [@wu-clan](https://github.com/wu-clan) in [#1115](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1115)
* Fix online api user id acquisition by [@wu-clan](https://github.com/wu-clan) in [#1116](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1116)
* Fix plugin status change cache missing by [@wu-clan](https://github.com/wu-clan) in [#1118](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1118)
* Fix zip plugin installation and unzip by [@wu-clan](https://github.com/wu-clan) in [#1120](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1120)
* Update plugin config and sql validate by [@wu-clan](https://github.com/wu-clan) in [#1122](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1122)
* Add sql scripts for OAuth2 plugin by [@wu-clan](https://github.com/wu-clan) in [#1121](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1121)
* Update the version number to 1.13.2 by [@wu-clan](https://github.com/wu-clan) in [#1123](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1123)


**Full Changelog**: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.1...v1.13.2

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.13.2]


<a id="v1.13.1"></a>
# [v1.13.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.13.1) - 2026-03-08

## What's Changed
* Update changelog for v1.13.0 by [@wu-clan](https://github.com/wu-clan) in [#1078](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1078)
* Fix task issues and update crontab expressions by [@wu-clan](https://github.com/wu-clan) in [#1080](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1080)
* Add redis client native OTEL observability by [@wu-clan](https://github.com/wu-clan) in [#1082](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1082)
* Add data permission rule value template variable by [@wu-clan](https://github.com/wu-clan) in [#1081](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1081)
* Update SQL scripts related to data permissions by [@wu-clan](https://github.com/wu-clan) in [#1084](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1084)
* Remove the sponsorship from the readme by [@wu-clan](https://github.com/wu-clan) in [#1085](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1085)
* Fix query sorting based on model sort column by [@wu-clan](https://github.com/wu-clan) in [#1083](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1083)
* Fix uninstall plugin requirements command by [@wu-clan](https://github.com/wu-clan) in [#1087](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1087)
* Add remove plugin and formatting code CLI by [@wu-clan](https://github.com/wu-clan) in [#1088](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1088)
* Refactor the menu SQL definition in SQL scripts by [@wu-clan](https://github.com/wu-clan) in [#1092](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1092)
* Add destroy SQL scripts for multiple plugins by [@wu-clan](https://github.com/wu-clan) in [#1093](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1093)
* Update the upload file type validation logic by [@SmallGarbage](https://github.com/SmallGarbage) in [#1091](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1091)
* Optimize the CLI command console output style by [@wu-clan](https://github.com/wu-clan) in [#1094](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1094)
* Fix menu SQL in mysql SQL scripts by [@wu-clan](https://github.com/wu-clan) in [#1096](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1096)
* Update project name symbol in multiple files by [@wu-clan](https://github.com/wu-clan) in [#1097](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1097)
* Update utc zoneinfo to datetime timezone by [@wu-clan](https://github.com/wu-clan) in [#1099](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1099)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [#1100](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1100)
* Update the version number to 1.13.1 by [@wu-clan](https://github.com/wu-clan) in [#1102](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1102)

## New Contributors
* [@SmallGarbage](https://github.com/SmallGarbage) made their first contribution in [#1091](https://github.com/fastapi-practices/fastapi-best-architecture/pull/1091)

**Full Changelog**: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.0...v1.13.1

## Contributors

<a href="https://github.com/SmallGarbage"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FSmallGarbage.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@SmallGarbage"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.13.1]


<a id="v1.13.0"></a>
# [v1.13.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.13.0) - 2026-02-14

## What's Changed
* Update changelog for v1.12.3 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1009](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1009)
* Update the JWT for easier scaling by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1011](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1011)
* Update the database and Redis for easier scaling by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1015](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1015)
* Fix database calls in init CLI command by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1016](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1016)
* Fix install plugin dependencies in docker container by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1017](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1017)
* Fix database engine in auto init CLI command by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1018](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1018)
* Rename locale to locales to avoid library conflict by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1021](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1021)
* Optimize dynamic config loading implementation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1022](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1022)
* Optimize i18n language file directory structure by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1023](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1023)
* Fix snowflake type primary key field serializer by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1024](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1024)
* Optimize code generation data processing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1020](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1020)
* Update the i18n file storage directory by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1027](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1027)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1029](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1029)
* Fix custom filename in code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1030](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1030)
* Add router jinja template for code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1031](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1031)
* Allow to add config in plugin toml by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1033](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1033)
* Refactor code generation and plugin hot reloading by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1032](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1032)
* Add injection app routes to code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1034](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1034)
* Remove deprecated parameter for code generation business by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1035](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1035)
* Add code generation preview mode CLI command by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1036](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1036)
* Update plugins and adapt to new features by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1040](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1040)
* Add data validator for plugin config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1041](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1041)
* Fix code generation app route injection by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1042](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1042)
* Update the plugin git address pattern by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1047](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1047)
* Update plugin and code generation subprocess output by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1048](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1048)
* Add the alembic related operation CLI by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1049](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1049)
* Update task path resolution and docker variables by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1050](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1050)
* Update redis and server health monitor data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1051](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1051)
* Add multi level caching and optimize caching by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1054](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1054)
* Add granian and celery metrics collection by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1057](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1057)
* Fix relational insertion error for empty lists by [@SoulEater](https://github.com/SoulEater) in [fastapi-practices/fastapi_best_architecture#1056](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1056)
* Optimize the serialization of join query results by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1058](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1058)
* Update alembic and ruff config to pyproject.toml by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1060](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1060)
* Add tombi toml and bump pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1061](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1061)
* Add tombi and plugin JSON schema config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1062](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1062)
* Fix multi level cache key build and usage by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1066](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1066)
* Add log mount to docker compose by [@yzbf-lin](https://github.com/yzbf-lin) in [fastapi-practices/fastapi_best_architecture#1063](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1063)
* Fix captcha and user validation order logic error by [@mic1on](https://github.com/mic1on) in [fastapi-practices/fastapi_best_architecture#1065](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1065)
* Add multi level cache for dynamic config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1067](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1067)
* Add version check and update workflows by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1068](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1068)
* Add cache key chaining syntax support by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1069](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1069)
* Refactor the interface rate limiter implementation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1072](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1072)
* Fix dynamic config cache serialization by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1075](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1075)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1076](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1076)
* Fix missing parent class init in base exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1077](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1077)
* Update the version number to 1.13.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1079](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1079)

## New Contributors
* [@SoulEater](https://github.com/SoulEater) made their first contribution in [fastapi-practices/fastapi_best_architecture#1056](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1056)
* [@mic1on](https://github.com/mic1on) made their first contribution in [fastapi-practices/fastapi_best_architecture#1065](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1065)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.12.3...v1.13.0

## Contributors

<a href="https://github.com/SoulEater"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FSoulEater.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@SoulEater"></a>
<a href="https://github.com/mic1on"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fmic1on.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@mic1on"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>
<a href="https://github.com/yzbf-lin"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fyzbf-lin.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@yzbf-lin"></a>

[Changes][v1.13.0]


<a id="v1.12.3"></a>
# [v1.12.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.12.3) - 2026-01-13

## What's Changed
* Update changelog for v1.12.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#995](https://github.com/fastapi-practices/fastapi_best_architecture/pull/995)
* Update login log request header column length by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#996](https://github.com/fastapi-practices/fastapi_best_architecture/pull/996)
* Fix opera log non-json data overload by [@shj366](https://github.com/shj366) in [fastapi-practices/fastapi_best_architecture#998](https://github.com/fastapi-practices/fastapi_best_architecture/pull/998)
* Remove the opera log desensitization asynchronous by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#999](https://github.com/fastapi-practices/fastapi_best_architecture/pull/999)
* Update redis and server monitor implementations by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1000](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1000)
* Optimize definitions of multiple utility functions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1001](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1001)
* Update code generation part file naming by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1002](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1002)
* Update nickname generation when create user by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1004](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1004)
* Update the plugin dependency install method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1007](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1007)
* Update i18n language storage and loading by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#1008](https://github.com/fastapi-practices/fastapi_best_architecture/pull/1008)

## New Contributors
* [@shj366](https://github.com/shj366) made their first contribution in [fastapi-practices/fastapi_best_architecture#998](https://github.com/fastapi-practices/fastapi_best_architecture/pull/998)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.12.2...v1.12.3

## Contributors

<a href="https://github.com/shj366"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fshj366.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@shj366"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.12.3]


<a id="v1.12.2"></a>
# [v1.12.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.12.2) - 2026-01-07

## What's Changed
* Update changelog for v1.12.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#983](https://github.com/fastapi-practices/fastapi_best_architecture/pull/983)
* Fix environment variable file auto init by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#985](https://github.com/fastapi-practices/fastapi_best_architecture/pull/985)
* Simplify the desensitization of operation log data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#987](https://github.com/fastapi-practices/fastapi_best_architecture/pull/987)
* Remove invalid configs of operation log by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#988](https://github.com/fastapi-practices/fastapi_best_architecture/pull/988)
* Fix operation log queue status management by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#989](https://github.com/fastapi-practices/fastapi_best_architecture/pull/989)
* Fix SQL scripts error in config plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#991](https://github.com/fastapi-practices/fastapi_best_architecture/pull/991)
* Fix the key of the refresh token removed by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#993](https://github.com/fastapi-practices/fastapi_best_architecture/pull/993)
* Remove Linux Do OAuth2 login by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#994](https://github.com/fastapi-practices/fastapi_best_architecture/pull/994)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.12.1...v1.12.2

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.12.2]


<a id="v1.12.1"></a>
# [v1.12.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.12.1) - 2025-12-31

## What's Changed
* Update changelog for v1.12.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#963](https://github.com/fastapi-practices/fastapi_best_architecture/pull/963)
* Update Grafana security and user default config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#964](https://github.com/fastapi-practices/fastapi_best_architecture/pull/964)
* Rename the pre start script to migrate by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#965](https://github.com/fastapi-practices/fastapi_best_architecture/pull/965)
* Add code generation and notice SQL scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#966](https://github.com/fastapi-practices/fastapi_best_architecture/pull/966)
* Fix support for special character passwords by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#968](https://github.com/fastapi-practices/fastapi_best_architecture/pull/968)
* Add an independent contribution document by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#971](https://github.com/fastapi-practices/fastapi_best_architecture/pull/971)
* Fix i18n target language error when concurrent by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#970](https://github.com/fastapi-practices/fastapi_best_architecture/pull/970)
* Add observability instrument for redis client by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#972](https://github.com/fastapi-practices/fastapi_best_architecture/pull/972)
* Add OTEL semantic specification metrics config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#973](https://github.com/fastapi-practices/fastapi_best_architecture/pull/973)
* Fix case where the user agent was empty by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#976](https://github.com/fastapi-practices/fastapi_best_architecture/pull/976)
* Optimize login log database session calls by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#977](https://github.com/fastapi-practices/fastapi_best_architecture/pull/977)
* Add the auto init project CLI command by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#978](https://github.com/fastapi-practices/fastapi_best_architecture/pull/978)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#979](https://github.com/fastapi-practices/fastapi_best_architecture/pull/979)
* Add observability instrument for httpx request by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#980](https://github.com/fastapi-practices/fastapi_best_architecture/pull/980)
* Update git and docker ignore files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#981](https://github.com/fastapi-practices/fastapi_best_architecture/pull/981)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.12.0...v1.12.1

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.12.1]


<a id="v1.12.0"></a>
# [v1.12.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.12.0) - 2025-12-15

## What's Changed
* Update changelog for v1.11.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#942](https://github.com/fastapi-practices/fastapi_best_architecture/pull/942)
* Update celery related docker container independence by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#943](https://github.com/fastapi-practices/fastapi_best_architecture/pull/943)
* Fix super value in update user permissions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#948](https://github.com/fastapi-practices/fastapi_best_architecture/pull/948)
* Optimize data permission logic and usage by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#947](https://github.com/fastapi-practices/fastapi_best_architecture/pull/947)
* Update pre-commit to prek in pre-commit script by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#949](https://github.com/fastapi-practices/fastapi_best_architecture/pull/949)
* Optimize the coupling of user social plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#950](https://github.com/fastapi-practices/fastapi_best_architecture/pull/950)
* Add the database primary key mode config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#953](https://github.com/fastapi-practices/fastapi_best_architecture/pull/953)
* Optimize the coupling of code generation CLI by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#951](https://github.com/fastapi-practices/fastapi_best_architecture/pull/951)
* Add CLI init project database support by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#952](https://github.com/fastapi-practices/fastapi_best_architecture/pull/952)
* Update the init project database CLI to subcommand by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#954](https://github.com/fastapi-practices/fastapi_best_architecture/pull/954)
* Fix CLI command for code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#956](https://github.com/fastapi-practices/fastapi_best_architecture/pull/956)
* Fix the IP address in the request log by [@wuyuemushi](https://github.com/wuyuemushi) in [fastapi-practices/fastapi_best_architecture#959](https://github.com/fastapi-practices/fastapi_best_architecture/pull/959)
* Add the Grafana observability suite by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#961](https://github.com/fastapi-practices/fastapi_best_architecture/pull/961)
* Update the version number to 1.12.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#962](https://github.com/fastapi-practices/fastapi_best_architecture/pull/962)

## New Contributors
* [@wuyuemushi](https://github.com/wuyuemushi) made their first contribution in [fastapi-practices/fastapi_best_architecture#959](https://github.com/fastapi-practices/fastapi_best_architecture/pull/959)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.11.2...v1.12.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>
<a href="https://github.com/wuyuemushi"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwuyuemushi.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wuyuemushi"></a>

[Changes][v1.12.0]


<a id="v1.11.2"></a>
# [v1.11.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.11.2) - 2025-11-28

## What's Changed
* Update changelog for v1.11.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#923](https://github.com/fastapi-practices/fastapi_best_architecture/pull/923)
* Fix typos in data rule sql scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#926](https://github.com/fastapi-practices/fastapi_best_architecture/pull/926)
* Restore captcha uuid naming in the login params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#928](https://github.com/fastapi-practices/fastapi_best_architecture/pull/928)
* Add distributed deployment support for snowflake ID by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#927](https://github.com/fastapi-practices/fastapi_best_architecture/pull/927)
* Add env reqs for plugin install and uninstall by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#929](https://github.com/fastapi-practices/fastapi_best_architecture/pull/929)
* Optimize the use of some LRU caches by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#932](https://github.com/fastapi-practices/fastapi_best_architecture/pull/932)
* Update the i18n language file init location by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#934](https://github.com/fastapi-practices/fastapi_best_architecture/pull/934)
* Fix get column types in code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#935](https://github.com/fastapi-practices/fastapi_best_architecture/pull/935)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#936](https://github.com/fastapi-practices/fastapi_best_architecture/pull/936)
* Update the files interface filename to file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#937](https://github.com/fastapi-practices/fastapi_best_architecture/pull/937)
* Update task application interface definitions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#938](https://github.com/fastapi-practices/fastapi_best_architecture/pull/938)
* Update code generation interface definitions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#939](https://github.com/fastapi-practices/fastapi_best_architecture/pull/939)
* Update the fba run CLI command output by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#941](https://github.com/fastapi-practices/fastapi_best_architecture/pull/941)
* Update the version number to 1.11.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#940](https://github.com/fastapi-practices/fastapi_best_architecture/pull/940)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.11.1...v1.11.2

## Contributors

<a href="https://github.com/downdawn"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdowndawn.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@downdawn"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.11.2]


<a id="v1.11.1"></a>
# [v1.11.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.11.1) - 2025-11-16

## What's Changed
* Update changelog for v1.11.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#917](https://github.com/fastapi-practices/fastapi_best_architecture/pull/917)
* Fix missing table in alembic migration by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#920](https://github.com/fastapi-practices/fastapi_best_architecture/pull/920)
* Add user social binding and unbinding by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#919](https://github.com/fastapi-practices/fastapi_best_architecture/pull/919)
* Fix the user list query serialization by [@linrong](https://github.com/linrong) in [fastapi-practices/fastapi_best_architecture#921](https://github.com/fastapi-practices/fastapi_best_architecture/pull/921)
* Update user and login security configs by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#922](https://github.com/fastapi-practices/fastapi_best_architecture/pull/922)

## New Contributors
* [@linrong](https://github.com/linrong) made their first contribution in [fastapi-practices/fastapi_best_architecture#921](https://github.com/fastapi-practices/fastapi_best_architecture/pull/921)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.11.0...v1.11.1

## Contributors

<a href="https://github.com/linrong"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Flinrong.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@linrong"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.11.1]


<a id="v1.11.0"></a>
# [v1.11.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.11.0) - 2025-11-12

## What's Changed
* Update changelog for v1.10.4 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#916](https://github.com/fastapi-practices/fastapi_best_architecture/pull/916)
* Refactor foreign keys and relationships to pure logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#901](https://github.com/fastapi-practices/fastapi_best_architecture/pull/901)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.10.4...v1.11.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.11.0]


<a id="v1.10.4"></a>
# [v1.10.4](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.10.4) - 2025-11-12

## What's Changed
* Update changelog for v1.10.3 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#895](https://github.com/fastapi-practices/fastapi_best_architecture/pull/895)
* Bump fastapi oauth2 from 0.0.1 to 0.0.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#896](https://github.com/fastapi-practices/fastapi_best_architecture/pull/896)
* Update the interface timing accuracy in log by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#897](https://github.com/fastapi-practices/fastapi_best_architecture/pull/897)
* Optimize redis batch get and delete operations by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#899](https://github.com/fastapi-practices/fastapi_best_architecture/pull/899)
* Update the time column type in the task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#900](https://github.com/fastapi-practices/fastapi_best_architecture/pull/900)
* Add the user social independent enum file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#902](https://github.com/fastapi-practices/fastapi_best_architecture/pull/902)
* Optimize the request params of the service layer by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#903](https://github.com/fastapi-practices/fastapi_best_architecture/pull/903)
* Optimize the data permission condition build by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#904](https://github.com/fastapi-practices/fastapi_best_architecture/pull/904)
* Fix response status codes in the request logs by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#905](https://github.com/fastapi-practices/fastapi_best_architecture/pull/905)
* Add dept validation to user updates by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#906](https://github.com/fastapi-practices/fastapi_best_architecture/pull/906)
* Update the version number to 1.10.4 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#907](https://github.com/fastapi-practices/fastapi_best_architecture/pull/907)
* Fix typo in the data permission prompt by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#909](https://github.com/fastapi-practices/fastapi_best_architecture/pull/909)
* Fix user cache cleanup when operating data rules by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#910](https://github.com/fastapi-practices/fastapi_best_architecture/pull/910)
* Fix create and delete department validations by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#911](https://github.com/fastapi-practices/fastapi_best_architecture/pull/911)
* Fix the user menu sidebar parsing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#912](https://github.com/fastapi-practices/fastapi_best_architecture/pull/912)
* Add user social unbinding account interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#913](https://github.com/fastapi-practices/fastapi_best_architecture/pull/913)
* Fix user cache cleanup when updating data scope by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#915](https://github.com/fastapi-practices/fastapi_best_architecture/pull/915)
* Fix dept and menu table subqueries by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#914](https://github.com/fastapi-practices/fastapi_best_architecture/pull/914)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.10.3...v1.10.4

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.10.4]


<a id="v1.10.3"></a>
# [v1.10.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.10.3) - 2025-10-30

## What's Changed
* Update changelog for v1.10.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#873](https://github.com/fastapi-practices/fastapi_best_architecture/pull/873)
* Fix docker default database env variables by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#874](https://github.com/fastapi-practices/fastapi_best_architecture/pull/874)
* Add port for fba sever in docker compose by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#875](https://github.com/fastapi-practices/fastapi_best_architecture/pull/875)
* Update the container naming in docker scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#876](https://github.com/fastapi-practices/fastapi_best_architecture/pull/876)
* Fix the httpurl type compatibility with postgresql by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#877](https://github.com/fastapi-practices/fastapi_best_architecture/pull/877)
* Update the default length of user email column by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#878](https://github.com/fastapi-practices/fastapi_best_architecture/pull/878)
* Update the serializer of httpurl type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#879](https://github.com/fastapi-practices/fastapi_best_architecture/pull/879)
* Fix the OAuth2 link acquisition in HTTPS by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#881](https://github.com/fastapi-practices/fastapi_best_architecture/pull/881)
* Add Google OAuth2 callback to opera log exclusion by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#882](https://github.com/fastapi-practices/fastapi_best_architecture/pull/882)
* Update the length style of the model columns by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#883](https://github.com/fastapi-practices/fastapi_best_architecture/pull/883)
* Bump dependencies to the latest version by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#890](https://github.com/fastapi-practices/fastapi_best_architecture/pull/890)
* Fix import in code generation api template by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#891](https://github.com/fastapi-practices/fastapi_best_architecture/pull/891)
* Fix celery compatibility with psycopg version by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#892](https://github.com/fastapi-practices/fastapi_best_architecture/pull/892)
* Fix the venv pip availability in Linux by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#893](https://github.com/fastapi-practices/fastapi_best_architecture/pull/893)
* Add the celery rabbitmq vhost config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#894](https://github.com/fastapi-practices/fastapi_best_architecture/pull/894)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.10.2...v1.10.3

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.10.3]


<a id="v1.10.2"></a>
# [v1.10.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.10.2) - 2025-10-21

## What's Changed
* Update the changelog for v1.10.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#869](https://github.com/fastapi-practices/fastapi_best_architecture/pull/869)
* Bump rtoml and uvicorn to support python 3.14 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#871](https://github.com/fastapi-practices/fastapi_best_architecture/pull/871)
* Optimize sqlalchemy types to simplify compatibility by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#870](https://github.com/fastapi-practices/fastapi_best_architecture/pull/870)
* Bump fastapi to remove warning for python 3.14 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#872](https://github.com/fastapi-practices/fastapi_best_architecture/pull/872)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.10.1...v1.10.2

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.10.2]


<a id="v1.10.1"></a>
# [v1.10.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.10.1) - 2025-10-18

## What's Changed
* Update the changelog for v1.10.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#864](https://github.com/fastapi-practices/fastapi_best_architecture/pull/864)
* Fix tasks related to deleting db logs by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#863](https://github.com/fastapi-practices/fastapi_best_architecture/pull/863)
* Fix the volume in the docker compose script by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#865](https://github.com/fastapi-practices/fastapi_best_architecture/pull/865)
* Update the release changelog workflow by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#867](https://github.com/fastapi-practices/fastapi_best_architecture/pull/867)
* Bump dependencies to the latest version by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#868](https://github.com/fastapi-practices/fastapi_best_architecture/pull/868)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.10.0...v1.10.1

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.10.1]


<a id="v1.10.0"></a>
# [v1.10.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.10.0) - 2025-10-17

## What's Changed
* Fix the import table cli command by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#860](https://github.com/fastapi-practices/fastapi_best_architecture/pull/860)
* Update unique judgment logic for dict data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#859](https://github.com/fastapi-practices/fastapi_best_architecture/pull/859)
* Fix the api ninja in code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#858](https://github.com/fastapi-practices/fastapi_best_architecture/pull/858)
* Fix dict plugin pgsql init script missing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#857](https://github.com/fastapi-practices/fastapi_best_architecture/pull/857)
* Update the changelog for v1.9.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#856](https://github.com/fastapi-practices/fastapi_best_architecture/pull/856)
* Fix ctx in validation exception handler by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#861](https://github.com/fastapi-practices/fastapi_best_architecture/pull/861)
* Update the primary database to postgresql by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#829](https://github.com/fastapi-practices/fastapi_best_architecture/pull/829)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.9.0...v1.10.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.10.0]


<a id="v1.9.0"></a>
# [v1.9.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.9.0) - 2025-10-16

## What's Changed
* Update changelog for v1.8.3 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#849](https://github.com/fastapi-practices/fastapi_best_architecture/pull/849)
* Bump fastapi and pydantic to the latest by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#851](https://github.com/fastapi-practices/fastapi_best_architecture/pull/851)
* Update superuser verify to dependency injection by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#852](https://github.com/fastapi-practices/fastapi_best_architecture/pull/852)
* Fix the superuser verify missing auth by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#854](https://github.com/fastapi-practices/fastapi_best_architecture/pull/854)
* Update request state usage to context variable by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#853](https://github.com/fastapi-practices/fastapi_best_architecture/pull/853)
* Fix safely of access ctx in exception handlers by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#855](https://github.com/fastapi-practices/fastapi_best_architecture/pull/855)
* Refactor the service layer db session call method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#850](https://github.com/fastapi-practices/fastapi_best_architecture/pull/850)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.8.3...v1.9.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.9.0]


<a id="v1.8.3"></a>
# [v1.8.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.8.3) - 2025-10-13

## What's Changed
* Update changelog for v1.8.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#841](https://github.com/fastapi-practices/fastapi_best_architecture/pull/841)
* Fix the pgsql script in dict plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#842](https://github.com/fastapi-practices/fastapi_best_architecture/pull/842)
* Fix SQL script syntax error in config plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#843](https://github.com/fastapi-practices/fastapi_best_architecture/pull/843)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#845](https://github.com/fastapi-practices/fastapi_best_architecture/pull/845)
* Update the ruff rules and format the code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#846](https://github.com/fastapi-practices/fastapi_best_architecture/pull/846)
* Bump fastapi and sqlalchemy to support python 3.14 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#847](https://github.com/fastapi-practices/fastapi_best_architecture/pull/847)
* Bump sqlalchemy-crud-plus from 0.12.0 to 0.12.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#848](https://github.com/fastapi-practices/fastapi_best_architecture/pull/848)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.8.2...v1.8.3

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.8.3]


<a id="v1.8.2"></a>
# [v1.8.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.8.2) - 2025-09-26

## What's Changed
* Update changelog for v1.8.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#804](https://github.com/fastapi-practices/fastapi_best_architecture/pull/804)
* Update the swagger docs version to dynamic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#805](https://github.com/fastapi-practices/fastapi_best_architecture/pull/805)
* Fix the subprocess ensurepip got stuck in Linux by [@byte-voyager](https://github.com/byte-voyager) in [fastapi-practices/fastapi_best_architecture#806](https://github.com/fastapi-practices/fastapi_best_architecture/pull/806)
* Update the offline location information parse by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#807](https://github.com/fastapi-practices/fastapi_best_architecture/pull/807)
* Fix pgsql syntax error in code generation by [@byte-voyager](https://github.com/byte-voyager) in [fastapi-practices/fastapi_best_architecture#808](https://github.com/fastapi-practices/fastapi_best_architecture/pull/808)
* Fix summary default in opera log middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#809](https://github.com/fastapi-practices/fastapi_best_architecture/pull/809)
* Fix special character password support in alembic by [@MortyZhaoy](https://github.com/MortyZhaoy) in [fastapi-practices/fastapi_best_architecture#811](https://github.com/fastapi-practices/fastapi_best_architecture/pull/811)
* Update the startup progress information display by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#812](https://github.com/fastapi-practices/fastapi_best_architecture/pull/812)
* Update the login captcha verify logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#815](https://github.com/fastapi-practices/fastapi_best_architecture/pull/815)
* Fix the summary in opera log middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#816](https://github.com/fastapi-practices/fastapi_best_architecture/pull/816)
* Update the dict plugin table structure by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#817](https://github.com/fastapi-practices/fastapi_best_architecture/pull/817)
* Add version number output to the startup CLI by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#820](https://github.com/fastapi-practices/fastapi_best_architecture/pull/820)
* Update the user agent in opera log model by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#831](https://github.com/fastapi-practices/fastapi_best_architecture/pull/831)
* Fix code generation template missing Decimal by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#830](https://github.com/fastapi-practices/fastapi_best_architecture/pull/830)
* Fix the get model object method return logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#832](https://github.com/fastapi-practices/fastapi_best_architecture/pull/832)
* Simplify the code generation CLI parameters by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#837](https://github.com/fastapi-practices/fastapi_best_architecture/pull/837)
* Add the refresh token to demo mode exclusion by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#834](https://github.com/fastapi-practices/fastapi_best_architecture/pull/834)
* Add extension parameters to paging data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#835](https://github.com/fastapi-practices/fastapi_best_architecture/pull/835)
* Fix the phone filter in the user list by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#838](https://github.com/fastapi-practices/fastapi_best_architecture/pull/838)
* Update docker and deployment script comments by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#839](https://github.com/fastapi-practices/fastapi_best_architecture/pull/839)
* Update the version number to 1.8.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#840](https://github.com/fastapi-practices/fastapi_best_architecture/pull/840)

## New Contributors
* [@byte-voyager](https://github.com/byte-voyager) made their first contribution in [fastapi-practices/fastapi_best_architecture#806](https://github.com/fastapi-practices/fastapi_best_architecture/pull/806)
* [@MortyZhaoy](https://github.com/MortyZhaoy) made their first contribution in [fastapi-practices/fastapi_best_architecture#811](https://github.com/fastapi-practices/fastapi_best_architecture/pull/811)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.8.1...v1.8.2

## Contributors

<a href="https://github.com/MortyZhaoy"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FMortyZhaoy.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@MortyZhaoy"></a>
<a href="https://github.com/byte-voyager"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fbyte-voyager.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@byte-voyager"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.8.2]


<a id="v1.8.1"></a>
# [v1.8.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.8.1) - 2025-09-09

## What's Changed
* Update changelog for v1.8.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#772](https://github.com/fastapi-practices/fastapi_best_architecture/pull/772)
* Optimize the celery crontab expression validation by [@yanlingsishao](https://github.com/yanlingsishao) in [fastapi-practices/fastapi_best_architecture#773](https://github.com/fastapi-practices/fastapi_best_architecture/pull/773)
* Add bulk update interface for config plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#774](https://github.com/fastapi-practices/fastapi_best_architecture/pull/774)
* Optimize email sending config update logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#775](https://github.com/fastapi-practices/fastapi_best_architecture/pull/775)
* Add test data SQL script for config plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#776](https://github.com/fastapi-practices/fastapi_best_architecture/pull/776)
* Update the env parameter value in env file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#777](https://github.com/fastapi-practices/fastapi_best_architecture/pull/777)
* Fix the docker compose env configuration file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#778](https://github.com/fastapi-practices/fastapi_best_architecture/pull/778)
* Fix redis client not close after plugin parse by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#780](https://github.com/fastapi-practices/fastapi_best_architecture/pull/780)
* Fix the celery beat distributed lock timeout by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#779](https://github.com/fastapi-practices/fastapi_best_architecture/pull/779)
* Fix the plugin model object detection logic by [@wuyao4](https://github.com/wuyao4) in [fastapi-practices/fastapi_best_architecture#782](https://github.com/fastapi-practices/fastapi_best_architecture/pull/782)
* Update the celery task result table creation logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#783](https://github.com/fastapi-practices/fastapi_best_architecture/pull/783)
* Fix code generation template params and filename by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#784](https://github.com/fastapi-practices/fastapi_best_architecture/pull/784)
* Fix CLI openapi url in production environment by [@siyue-wang](https://github.com/siyue-wang) in [fastapi-practices/fastapi_best_architecture#785](https://github.com/fastapi-practices/fastapi_best_architecture/pull/785)
* Update the model datetime column type to custom by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#786](https://github.com/fastapi-practices/fastapi_best_architecture/pull/786)
* Update the opera log exception message record by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#788](https://github.com/fastapi-practices/fastapi_best_architecture/pull/788)
* Update the handling of CORS 500 status code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#789](https://github.com/fastapi-practices/fastapi_best_architecture/pull/789)
* Add the Google OAuth2 login by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#790](https://github.com/fastapi-practices/fastapi_best_architecture/pull/790)
* Fix the tzinfo comparison in the timezone type by [@IAseven](https://github.com/IAseven) in [fastapi-practices/fastapi_best_architecture#787](https://github.com/fastapi-practices/fastapi_best_architecture/pull/787)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#791](https://github.com/fastapi-practices/fastapi_best_architecture/pull/791)
* Update the notice model and pagination by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#792](https://github.com/fastapi-practices/fastapi_best_architecture/pull/792)
* Add the dict type query all interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#794](https://github.com/fastapi-practices/fastapi_best_architecture/pull/794)
* Fix sql script syntax error in config plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#793](https://github.com/fastapi-practices/fastapi_best_architecture/pull/793)
* Fix the psycopg dependency naming by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#795](https://github.com/fastapi-practices/fastapi_best_architecture/pull/795)
* Add schema for the tree data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#796](https://github.com/fastapi-practices/fastapi_best_architecture/pull/796)
* Add the code generator to the CLI by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#798](https://github.com/fastapi-practices/fastapi_best_architecture/pull/798)
* Optimize the code generation interaction logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#799](https://github.com/fastapi-practices/fastapi_best_architecture/pull/799)
* Fix console import in main module by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#800](https://github.com/fastapi-practices/fastapi_best_architecture/pull/800)
* Fix the subprocess check call failed in windows by [@yzbf-lin](https://github.com/yzbf-lin) in [fastapi-practices/fastapi_best_architecture#802](https://github.com/fastapi-practices/fastapi_best_architecture/pull/802)
* Fix alembic migration file missing import by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#803](https://github.com/fastapi-practices/fastapi_best_architecture/pull/803)

## New Contributors
* [@yanlingsishao](https://github.com/yanlingsishao) made their first contribution in [fastapi-practices/fastapi_best_architecture#773](https://github.com/fastapi-practices/fastapi_best_architecture/pull/773)
* [@wuyao4](https://github.com/wuyao4) made their first contribution in [fastapi-practices/fastapi_best_architecture#782](https://github.com/fastapi-practices/fastapi_best_architecture/pull/782)
* [@siyue-wang](https://github.com/siyue-wang) made their first contribution in [fastapi-practices/fastapi_best_architecture#785](https://github.com/fastapi-practices/fastapi_best_architecture/pull/785)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.8.0...v1.8.1

## Contributors

<a href="https://github.com/IAseven"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FIAseven.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@IAseven"></a>
<a href="https://github.com/siyue-wang"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fsiyue-wang.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@siyue-wang"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>
<a href="https://github.com/wuyao4"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwuyao4.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wuyao4"></a>
<a href="https://github.com/yanlingsishao"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fyanlingsishao.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@yanlingsishao"></a>
<a href="https://github.com/yzbf-lin"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fyzbf-lin.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@yzbf-lin"></a>

[Changes][v1.8.1]


<a id="v1.8.0"></a>
# [v1.8.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.8.0) - 2025-08-15

## What's Changed
* Update changelog for v1.7.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#729](https://github.com/fastapi-practices/fastapi_best_architecture/pull/729)
* Simplify task crontab expression validation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#733](https://github.com/fastapi-practices/fastapi_best_architecture/pull/733)
* Add distributed lock for scheduled task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#732](https://github.com/fastapi-practices/fastapi_best_architecture/pull/732)
* Update the default cache period for userinfo by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#734](https://github.com/fastapi-practices/fastapi_best_architecture/pull/734)
* Fix celery CLI option to required by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#737](https://github.com/fastapi-practices/fastapi_best_architecture/pull/737)
* Add auth whitelist regular expression config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#738](https://github.com/fastapi-practices/fastapi_best_architecture/pull/738)
* Fix the opera log field encryption by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#739](https://github.com/fastapi-practices/fastapi_best_architecture/pull/739)
* Update the OAuth2 login password policy by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#741](https://github.com/fastapi-practices/fastapi_best_architecture/pull/741)
* Add update support for user email and phone by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#742](https://github.com/fastapi-practices/fastapi_best_architecture/pull/742)
* Fix the error trigger when model auto import by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#743](https://github.com/fastapi-practices/fastapi_best_architecture/pull/743)
* Simplify the plugin status update logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#744](https://github.com/fastapi-practices/fastapi_best_architecture/pull/744)
* Add some interfaces for user profiles by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#745](https://github.com/fastapi-practices/fastapi_best_architecture/pull/745)
* Add schedule task demo that contains params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#746](https://github.com/fastapi-practices/fastapi_best_architecture/pull/746)
* Fix the kwargs params of schedule task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#747](https://github.com/fastapi-practices/fastapi_best_architecture/pull/747)
* Refactor code generation files and routes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#748](https://github.com/fastapi-practices/fastapi_best_architecture/pull/748)
* Refactor task routes and add control routes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#749](https://github.com/fastapi-practices/fastapi_best_architecture/pull/749)
* Fix message format in validation exception handler by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#755](https://github.com/fastapi-practices/fastapi_best_architecture/pull/755)
* Update the opera log desensitization method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#756](https://github.com/fastapi-practices/fastapi_best_architecture/pull/756)
* Add business pagination in the code generator by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#757](https://github.com/fastapi-practices/fastapi_best_architecture/pull/757)
* Optimize the data sort logic of tree nodes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#758](https://github.com/fastapi-practices/fastapi_best_architecture/pull/758)
* Update log output config and format by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#759](https://github.com/fastapi-practices/fastapi_best_architecture/pull/759)
* Update the naming of table creation function by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#760](https://github.com/fastapi-practices/fastapi_best_architecture/pull/760)
* Optimize the opera log storage logic through queue by [@IAseven](https://github.com/IAseven) in [fastapi-practices/fastapi_best_architecture#750](https://github.com/fastapi-practices/fastapi_best_architecture/pull/750)
* Optimize naming and preview in code generation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#764](https://github.com/fastapi-practices/fastapi_best_architecture/pull/764)
* Update the description for the run file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#766](https://github.com/fastapi-practices/fastapi_best_architecture/pull/766)
* Optimize the timezone datetime return encoder by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#767](https://github.com/fastapi-practices/fastapi_best_architecture/pull/767)
* Update the content layout of the config file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#768](https://github.com/fastapi-practices/fastapi_best_architecture/pull/768)
* Add a standalone email sending plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#769](https://github.com/fastapi-practices/fastapi_best_architecture/pull/769)
* Add i18n support for response message by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#753](https://github.com/fastapi-practices/fastapi_best_architecture/pull/753)
* Update the menu title in SQL scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#770](https://github.com/fastapi-practices/fastapi_best_architecture/pull/770)
* Update the version number to 1.8.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#771](https://github.com/fastapi-practices/fastapi_best_architecture/pull/771)

## New Contributors
* [@IAseven](https://github.com/IAseven) made their first contribution in [fastapi-practices/fastapi_best_architecture#750](https://github.com/fastapi-practices/fastapi_best_architecture/pull/750)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.7.0...v1.8.0

## Contributors

<a href="https://github.com/IAseven"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FIAseven.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@IAseven"></a>
<a href="https://github.com/downdawn"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdowndawn.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@downdawn"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.8.0]


<a id="v1.7.0"></a>
# [v1.7.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.7.0) - 2025-07-16

## What's Changed
* Update the changelog for v1.6.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#703](https://github.com/fastapi-practices/fastapi_best_architecture/pull/703)
* Update the CLI to be executed async by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#704](https://github.com/fastapi-practices/fastapi_best_architecture/pull/704)
* Fix the code generation schema template by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#706](https://github.com/fastapi-practices/fastapi_best_architecture/pull/706)
* Replace gunicorn deployment to granian by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#705](https://github.com/fastapi-practices/fastapi_best_architecture/pull/705)
* Fix the code generation delete schema template by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#708](https://github.com/fastapi-practices/fastapi_best_architecture/pull/708)
* Update the refresh token verify mechanism by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#710](https://github.com/fastapi-practices/fastapi_best_architecture/pull/710)
* Update the reload excludes for CLI run by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#709](https://github.com/fastapi-practices/fastapi_best_architecture/pull/709)
* Add CLI support for execute sql scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#711](https://github.com/fastapi-practices/fastapi_best_architecture/pull/711)
* Update the granian env to command params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#712](https://github.com/fastapi-practices/fastapi_best_architecture/pull/712)
* Update the middleware logging accuracy by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#713](https://github.com/fastapi-practices/fastapi_best_architecture/pull/713)
* Update the log output default style by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#714](https://github.com/fastapi-practices/fastapi_best_architecture/pull/714)
* Optimize the analysis of get plugins by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#716](https://github.com/fastapi-practices/fastapi_best_architecture/pull/716)
* Simplify user permission database queries by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#717](https://github.com/fastapi-practices/fastapi_best_architecture/pull/717)
* Update the CLI startup service mode by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#718](https://github.com/fastapi-practices/fastapi_best_architecture/pull/718)
* Add support for celery dynamic tasks by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#715](https://github.com/fastapi-practices/fastapi_best_architecture/pull/715)
* Fix the celery task scheduler query by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#719](https://github.com/fastapi-practices/fastapi_best_architecture/pull/719)
* Update the celery task comment and name by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#720](https://github.com/fastapi-practices/fastapi_best_architecture/pull/720)
* Optimize celery integrations and events by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#721](https://github.com/fastapi-practices/fastapi_best_architecture/pull/721)
* Simplify celery task crontab config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#722](https://github.com/fastapi-practices/fastapi_best_architecture/pull/722)
* Delete the default value of schema enum data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#723](https://github.com/fastapi-practices/fastapi_best_architecture/pull/723)
* Fix the parsing of execution task params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#725](https://github.com/fastapi-practices/fastapi_best_architecture/pull/725)
* Bump granian from 2.4.0 to 2.4.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#727](https://github.com/fastapi-practices/fastapi_best_architecture/pull/727)
* Add CLI support for startup celery services by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#724](https://github.com/fastapi-practices/fastapi_best_architecture/pull/724)
* Fix login and operation log clearing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#728](https://github.com/fastapi-practices/fastapi_best_architecture/pull/728)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.6.0...v1.7.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.7.0]


<a id="v1.6.0"></a>
# [v1.6.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.6.0) - 2025-06-30

## What's Changed
* Update changelog for v1.5.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#690](https://github.com/fastapi-practices/fastapi_best_architecture/pull/690)
* Optimize dict create and update logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#691](https://github.com/fastapi-practices/fastapi_best_architecture/pull/691)
* Fix the OAuth2 redirect route names by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#693](https://github.com/fastapi-practices/fastapi_best_architecture/pull/693)
* Update the SQL to adapt frontend plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#694](https://github.com/fastapi-practices/fastapi_best_architecture/pull/694)
* Update the extension plugin config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#695](https://github.com/fastapi-practices/fastapi_best_architecture/pull/695)
* Add the test user to SQL scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#696](https://github.com/fastapi-practices/fastapi_best_architecture/pull/696)
* Add custom CLI for service startup by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#697](https://github.com/fastapi-practices/fastapi_best_architecture/pull/697)
* Add CLI support for plugin install by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#698](https://github.com/fastapi-practices/fastapi_best_architecture/pull/698)
* Update the help for CLI run worker by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#699](https://github.com/fastapi-practices/fastapi_best_architecture/pull/699)
* Optimize the installation of plugin dependencies by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#700](https://github.com/fastapi-practices/fastapi_best_architecture/pull/700)
* Update the Dockerfile to adapt latest code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#701](https://github.com/fastapi-practices/fastapi_best_architecture/pull/701)
* Update the version number to 1.6.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#702](https://github.com/fastapi-practices/fastapi_best_architecture/pull/702)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.5.2...v1.6.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.6.0]


<a id="v1.5.2"></a>
# [v1.5.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.5.2) - 2025-06-24

## What's Changed
* Update changelog for v1.5.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#671](https://github.com/fastapi-practices/fastapi_best_architecture/pull/671)
* Fix some error class import by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#672](https://github.com/fastapi-practices/fastapi_best_architecture/pull/672)
* Optimize routes to better align with RESTful by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#673](https://github.com/fastapi-practices/fastapi_best_architecture/pull/673)
* Add the snowflake ID sql script by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#675](https://github.com/fastapi-practices/fastapi_best_architecture/pull/675)
* Optimize token detection and caching logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#677](https://github.com/fastapi-practices/fastapi_best_architecture/pull/677)
* Update cache cleanup for logout interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#678](https://github.com/fastapi-practices/fastapi_best_architecture/pull/678)
* Add dictionary type and datas queries by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#679](https://github.com/fastapi-practices/fastapi_best_architecture/pull/679)
* Optimize api with semantic HTTP status codes by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#681](https://github.com/fastapi-practices/fastapi_best_architecture/pull/681)
* Fix the code with outdated system config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#683](https://github.com/fastapi-practices/fastapi_best_architecture/pull/683)
* Update dict data label column config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#684](https://github.com/fastapi-practices/fastapi_best_architecture/pull/684)
* Update the init test data for SQL scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#685](https://github.com/fastapi-practices/fastapi_best_architecture/pull/685)
* Simplify custom response status codes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#686](https://github.com/fastapi-practices/fastapi_best_architecture/pull/686)
* Optimize the zip plug-in file name parsing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#687](https://github.com/fastapi-practices/fastapi_best_architecture/pull/687)
* Add built-in plugin missing files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#688](https://github.com/fastapi-practices/fastapi_best_architecture/pull/688)
* Update the dict pagination query parameters by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#689](https://github.com/fastapi-practices/fastapi_best_architecture/pull/689)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.5.1...v1.5.2

## Contributors

<a href="https://github.com/downdawn"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdowndawn.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@downdawn"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.5.2]


<a id="v1.5.1"></a>
# [v1.5.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.5.1) - 2025-06-16

## What's Changed
* Update changelog for v1.5.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#664](https://github.com/fastapi-practices/fastapi_best_architecture/pull/664)
* Fix the sidebar menu type filtering by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#667](https://github.com/fastapi-practices/fastapi_best_architecture/pull/667)
* Bump sqlalchemy crud plus version to 1.10.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#668](https://github.com/fastapi-practices/fastapi_best_architecture/pull/668)
* Fix the postgresql sql script syntax error by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#669](https://github.com/fastapi-practices/fastapi_best_architecture/pull/669)
* Add Initial Snowflake ID Support by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#670](https://github.com/fastapi-practices/fastapi_best_architecture/pull/670)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.5.0...v1.5.1

## Contributors

<a href="https://github.com/downdawn"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdowndawn.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@downdawn"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.5.1]


<a id="v1.5.0"></a>
# [v1.5.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.5.0) - 2025-06-09

## What's Changed
* Update changelog for v1.4.3 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#651](https://github.com/fastapi-practices/fastapi_best_architecture/pull/651)
* Update OAuth2 callback interface return by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#653](https://github.com/fastapi-practices/fastapi_best_architecture/pull/653)
* Update user email and phone operation logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#654](https://github.com/fastapi-practices/fastapi_best_architecture/pull/654)
* Simplify OAuth2 model and optimize auth service by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#655](https://github.com/fastapi-practices/fastapi_best_architecture/pull/655)
* Add OAuth2 user to auto bind a role by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#656](https://github.com/fastapi-practices/fastapi_best_architecture/pull/656)
* Update data scope and rule to m2m by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#657](https://github.com/fastapi-practices/fastapi_best_architecture/pull/657)
* Update code generate interface permission by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#658](https://github.com/fastapi-practices/fastapi_best_architecture/pull/658)
* Update the plugin download interface permission by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#659](https://github.com/fastapi-practices/fastapi_best_architecture/pull/659)
* Update auth failed default status code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#660](https://github.com/fastapi-practices/fastapi_best_architecture/pull/660)
* Update menu sort in init test sql by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#661](https://github.com/fastapi-practices/fastapi_best_architecture/pull/661)
* Add data permission in init test sql by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#662](https://github.com/fastapi-practices/fastapi_best_architecture/pull/662)
* Update the version to 1.5.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#663](https://github.com/fastapi-practices/fastapi_best_architecture/pull/663)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.4.3...v1.5.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.5.0]


<a id="v1.4.3"></a>
# [v1.4.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.4.3) - 2025-06-02

## What's Changed
* Update changelog for v1.4.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#639](https://github.com/fastapi-practices/fastapi_best_architecture/pull/639)
* Fix the role update business variables by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#640](https://github.com/fastapi-practices/fastapi_best_architecture/pull/640)
* Fix the menu delete interface arg description by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#641](https://github.com/fastapi-practices/fastapi_best_architecture/pull/641)
* Fix the filter of query all menus by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#642](https://github.com/fastapi-practices/fastapi_best_architecture/pull/642)
* Refactor routes to better align with RESTful by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#645](https://github.com/fastapi-practices/fastapi_best_architecture/pull/645)
* Update the server startup time to string by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#646](https://github.com/fastapi-practices/fastapi_best_architecture/pull/646)
* Add get all data scope rules interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#647](https://github.com/fastapi-practices/fastapi_best_architecture/pull/647)
* Add data permission condition for filter data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#648](https://github.com/fastapi-practices/fastapi_best_architecture/pull/648)
* Update default value for role filter scopes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#649](https://github.com/fastapi-practices/fastapi_best_architecture/pull/649)
* Fix data permission condition for filter data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#650](https://github.com/fastapi-practices/fastapi_best_architecture/pull/650)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.4.2...v1.4.3

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.4.3]


<a id="v1.4.2"></a>
# [v1.4.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.4.2) - 2025-05-29

## What's Changed
* Update changelog for v1.4.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#630](https://github.com/fastapi-practices/fastapi_best_architecture/pull/630)
* Update non-linked sidebar support by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#633](https://github.com/fastapi-practices/fastapi_best_architecture/pull/633)
* Update the captcha invalidation error class by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#634](https://github.com/fastapi-practices/fastapi_best_architecture/pull/634)
* Optimize role-related data processing performance by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#635](https://github.com/fastapi-practices/fastapi_best_architecture/pull/635)
* Optimize install and build of plugin zip by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#636](https://github.com/fastapi-practices/fastapi_best_architecture/pull/636)
* Fix auto-increment id for postgres init data by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#632](https://github.com/fastapi-practices/fastapi_best_architecture/pull/632)
* Fix: prevent overwriting existing init files in code generator by [@lin-wu-1990](https://github.com/lin-wu-1990) in [fastapi-practices/fastapi_best_architecture#637](https://github.com/fastapi-practices/fastapi_best_architecture/pull/637)
* Simplify the user info update business by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#638](https://github.com/fastapi-practices/fastapi_best_architecture/pull/638)

## New Contributors
* [@lin-wu-1990](https://github.com/lin-wu-1990) made their first contribution in [fastapi-practices/fastapi_best_architecture#637](https://github.com/fastapi-practices/fastapi_best_architecture/pull/637)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.4.1...v1.4.2

## Contributors

<a href="https://github.com/huyuwei1996"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fhuyuwei1996.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@huyuwei1996"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.4.2]


<a id="v1.4.1"></a>
# [v1.4.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.4.1) - 2025-05-25

## What's Changed
* Update changelog for v1.4.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#621](https://github.com/fastapi-practices/fastapi_best_architecture/pull/621)
* Update the menu path and type columns by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#622](https://github.com/fastapi-practices/fastapi_best_architecture/pull/622)
* Add the deepwiki badge to README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#623](https://github.com/fastapi-practices/fastapi_best_architecture/pull/623)
* Refactor the system token to online users by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#624](https://github.com/fastapi-practices/fastapi_best_architecture/pull/624)
* Update the token check for logout interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#625](https://github.com/fastapi-practices/fastapi_best_architecture/pull/625)
* Update the token decode for logout interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#629](https://github.com/fastapi-practices/fastapi_best_architecture/pull/629)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.4.0...v1.4.1

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.4.1]


<a id="v1.4.0"></a>
# [v1.4.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.4.0) - 2025-05-22

## What's Changed
* Update changelog for v1.3.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#605](https://github.com/fastapi-practices/fastapi_best_architecture/pull/605)
* Add new plugin status check interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#606](https://github.com/fastapi-practices/fastapi_best_architecture/pull/606)
* Update the new plugin status to changed by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#607](https://github.com/fastapi-practices/fastapi_best_architecture/pull/607)
* Fix the task result schema param type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#611](https://github.com/fastapi-practices/fastapi_best_architecture/pull/611)
* Fix the plugin status update logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#613](https://github.com/fastapi-practices/fastapi_best_architecture/pull/613)
* Update uninstall and build plugin api method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#614](https://github.com/fastapi-practices/fastapi_best_architecture/pull/614)
* Fix non-asyncio nested async IO by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#610](https://github.com/fastapi-practices/fastapi_best_architecture/pull/610)
* Update the build plugin api params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#615](https://github.com/fastapi-practices/fastapi_best_architecture/pull/615)
* Update uv installation in docker deploy by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#619](https://github.com/fastapi-practices/fastapi_best_architecture/pull/619)
* Update the OAuth2 module to plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#620](https://github.com/fastapi-practices/fastapi_best_architecture/pull/620)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.3.0...v1.4.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.4.0]


<a id="v1.3.0"></a>
# [v1.3.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.3.0) - 2025-05-16

## What's Changed
* Update changelog for v1.2.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#598](https://github.com/fastapi-practices/fastapi_best_architecture/pull/598)
* Simplify apps and plugins config method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#600](https://github.com/fastapi-practices/fastapi_best_architecture/pull/600)
* Add plugin info config and interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#601](https://github.com/fastapi-practices/fastapi_best_architecture/pull/601)
* Fix the fastapi cli startup event loop by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#602](https://github.com/fastapi-practices/fastapi_best_architecture/pull/602)
* Optimize the zip plugin install logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#603](https://github.com/fastapi-practices/fastapi_best_architecture/pull/603)
* Update the casbin RBAC module path by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#604](https://github.com/fastapi-practices/fastapi_best_architecture/pull/604)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.2.0...v1.3.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.3.0]


<a id="v1.2.0"></a>
# [v1.2.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.2.0) - 2025-05-01

## What's Changed
* Update changelog for v1.1.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#589](https://github.com/fastapi-practices/fastapi_best_architecture/pull/589)
* Update code generator table columns by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#590](https://github.com/fastapi-practices/fastapi_best_architecture/pull/590)
* Update the default RBAC solution by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#593](https://github.com/fastapi-practices/fastapi_best_architecture/pull/593)
* Optimize the server information retrieval by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#595](https://github.com/fastapi-practices/fastapi_best_architecture/pull/595)
* Refactor the data rule to scope rule by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#596](https://github.com/fastapi-practices/fastapi_best_architecture/pull/596)
* Update the SQL script for creat tables by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#597](https://github.com/fastapi-practices/fastapi_best_architecture/pull/597)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.1.2...v1.2.0

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.2.0]


<a id="v1.1.2"></a>
# [v1.1.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.1.2) - 2025-04-23

## What's Changed
* Update the changelog for v1.1.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#583](https://github.com/fastapi-practices/fastapi_best_architecture/pull/583)
* Fix the condition to query menu by title by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#584](https://github.com/fastapi-practices/fastapi_best_architecture/pull/584)
* Fix cache cleanup when updating role menu by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#585](https://github.com/fastapi-practices/fastapi_best_architecture/pull/585)
* Optimize the userinfo cache cleaning logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#586](https://github.com/fastapi-practices/fastapi_best_architecture/pull/586)
* Bump fastapi pagination from 0.12.34 to 0.13.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#587](https://github.com/fastapi-practices/fastapi_best_architecture/pull/587)
* Update the routing style of the task app by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#588](https://github.com/fastapi-practices/fastapi_best_architecture/pull/588)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.1.1...v1.1.2

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.1.2]


<a id="v1.1.1"></a>
# [v1.1.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.1.1) - 2025-04-18

## What's Changed
* Update changelog for v1.1.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#580](https://github.com/fastapi-practices/fastapi_best_architecture/pull/580)
* Fix the plugin system route injection by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#581](https://github.com/fastapi-practices/fastapi_best_architecture/pull/581)
* Fix list query in the dict plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#582](https://github.com/fastapi-practices/fastapi_best_architecture/pull/582)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.1.0...v1.1.1

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.1.1]


<a id="v1.1.0"></a>
# [v1.1.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.1.0) - 2025-04-17

## What's Changed
* Update the changelog for v1.0.5 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#572](https://github.com/fastapi-practices/fastapi_best_architecture/pull/572)
* Update the default value for some functions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#573](https://github.com/fastapi-practices/fastapi_best_architecture/pull/573)
* Optimize the file structure of code generator by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#574](https://github.com/fastapi-practices/fastapi_best_architecture/pull/574)
* Update casbin RBAC verify to dynamic import by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#576](https://github.com/fastapi-practices/fastapi_best_architecture/pull/576)
* Update unique columns in dict models by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#577](https://github.com/fastapi-practices/fastapi_best_architecture/pull/577)
* Update the code generator to plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#578](https://github.com/fastapi-practices/fastapi_best_architecture/pull/578)
* Fix avatar url type of update avatar by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#575](https://github.com/fastapi-practices/fastapi_best_architecture/pull/575)
* Update code generator file and table naming by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#579](https://github.com/fastapi-practices/fastapi_best_architecture/pull/579)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.5...v1.1.0

## Contributors

<a href="https://github.com/huyuwei1996"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fhuyuwei1996.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@huyuwei1996"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.1.0]


<a id="v1.0.5"></a>
# [v1.0.5](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.5) - 2025-04-09

## What's Changed
* Update the changelog for v1.0.4 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#558](https://github.com/fastapi-practices/fastapi_best_architecture/pull/558)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#559](https://github.com/fastapi-practices/fastapi_best_architecture/pull/559)
* Add python 3.13 to GitHub ci by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#560](https://github.com/fastapi-practices/fastapi_best_architecture/pull/560)
* Update the system config to plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#561](https://github.com/fastapi-practices/fastapi_best_architecture/pull/561)
* Update dict data and type to plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#562](https://github.com/fastapi-practices/fastapi_best_architecture/pull/562)
* Update menu and add vben5 compatibility by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#563](https://github.com/fastapi-practices/fastapi_best_architecture/pull/563)
* Update the vben5 tree data structure by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#564](https://github.com/fastapi-practices/fastapi_best_architecture/pull/564)
* Update custom validation error messages by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#566](https://github.com/fastapi-practices/fastapi_best_architecture/pull/566)
* Update the number of pagination le by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#565](https://github.com/fastapi-practices/fastapi_best_architecture/pull/565)
* Fix the login password verification by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#568](https://github.com/fastapi-practices/fastapi_best_architecture/pull/568)
* Fix the failure hook of celery task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#569](https://github.com/fastapi-practices/fastapi_best_architecture/pull/569)
* Bump fastapi oauth2 from 0.0.1a2 to 0.0.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#570](https://github.com/fastapi-practices/fastapi_best_architecture/pull/570)
* Fix the log rule in gitignore by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#571](https://github.com/fastapi-practices/fastapi_best_architecture/pull/571)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.4...v1.0.5

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.0.5]


<a id="v1.0.4"></a>
# [v1.0.4](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.4) - 2025-03-28

## What's Changed
* Update the changelog for v1.0.3 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#543](https://github.com/fastapi-practices/fastapi_best_architecture/pull/543)
* Updated the backend contribution guide by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#544](https://github.com/fastapi-practices/fastapi_best_architecture/pull/544)
* Optimize the return of relationship interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#545](https://github.com/fastapi-practices/fastapi_best_architecture/pull/545)
* Optimize the dynamic import of data models by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#546](https://github.com/fastapi-practices/fastapi_best_architecture/pull/546)
* Update git and docker ignore files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#547](https://github.com/fastapi-practices/fastapi_best_architecture/pull/547)
* Optimize dependencies to reduce package size by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#548](https://github.com/fastapi-practices/fastapi_best_architecture/pull/548)
* Fix async install plugin dependencies for windows by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#549](https://github.com/fastapi-practices/fastapi_best_architecture/pull/549)
* Fix return schema of the config api by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#551](https://github.com/fastapi-practices/fastapi_best_architecture/pull/551)
* Optimize schemas with model relationships by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#552](https://github.com/fastapi-practices/fastapi_best_architecture/pull/552)
* Fix filters for opera log query list by [@ThankCat](https://github.com/ThankCat) in [fastapi-practices/fastapi_best_architecture#554](https://github.com/fastapi-practices/fastapi_best_architecture/pull/554)
* Fix the celery env in docker compose by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#555](https://github.com/fastapi-practices/fastapi_best_architecture/pull/555)
* Update volumes of redis in docker compose by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#556](https://github.com/fastapi-practices/fastapi_best_architecture/pull/556)
* Fix the query for the sub department by [@PoetryL](https://github.com/PoetryL) in [fastapi-practices/fastapi_best_architecture#557](https://github.com/fastapi-practices/fastapi_best_architecture/pull/557)
* Optimize codes and comments with cursor by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#550](https://github.com/fastapi-practices/fastapi_best_architecture/pull/550)

## New Contributors
* [@ThankCat](https://github.com/ThankCat) made their first contribution in [fastapi-practices/fastapi_best_architecture#554](https://github.com/fastapi-practices/fastapi_best_architecture/pull/554)
* [@PoetryL](https://github.com/PoetryL) made their first contribution in [fastapi-practices/fastapi_best_architecture#557](https://github.com/fastapi-practices/fastapi_best_architecture/pull/557)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.3...v1.0.4

## Contributors

<a href="https://github.com/PoetryL"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FPoetryL.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@PoetryL"></a>
<a href="https://github.com/ThankCat"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FThankCat.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@ThankCat"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.0.4]


<a id="v1.0.3"></a>
# [v1.0.3](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.3) - 2025-03-11

## What's Changed
* Update the changelog for v1.0.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#536](https://github.com/fastapi-practices/fastapi_best_architecture/pull/536)
* Update docker scripts in backend README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#537](https://github.com/fastapi-practices/fastapi_best_architecture/pull/537)
* Refactor toml and dependencies file dir by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#538](https://github.com/fastapi-practices/fastapi_best_architecture/pull/538)
* Fix typos in Dockerfile comments by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#539](https://github.com/fastapi-practices/fastapi_best_architecture/pull/539)
* Fix Dockerfile mounts for dependency installation by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#540](https://github.com/fastapi-practices/fastapi_best_architecture/pull/540)
* Add Aliyun mirror to PyPI index in pyproject.toml by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#541](https://github.com/fastapi-practices/fastapi_best_architecture/pull/541)
* Update docker scripts and nginx conf by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#542](https://github.com/fastapi-practices/fastapi_best_architecture/pull/542)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.2...v1.0.3

## Contributors

<a href="https://github.com/huyuwei1996"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fhuyuwei1996.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@huyuwei1996"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.0.3]


<a id="v1.0.2"></a>
# [v1.0.2](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.2) - 2025-03-01

## What's Changed
* Update the changelog for v1.0.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#532](https://github.com/fastapi-practices/fastapi_best_architecture/pull/532)
* Fix celery async task worker pool by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#533](https://github.com/fastapi-practices/fastapi_best_architecture/pull/533)
* Add log module root and output levels by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#534](https://github.com/fastapi-practices/fastapi_best_architecture/pull/534)
* Add plugin related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#535](https://github.com/fastapi-practices/fastapi_best_architecture/pull/535)


**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.1...v1.0.2

## Contributors

<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.0.2]


<a id="v1.0.1"></a>
# [v1.0.1](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.1) - 2025-02-26

## What's Changed
* Update the changelog for v1.0.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#524](https://github.com/fastapi-practices/fastapi_best_architecture/pull/524)
* Add missing volume config for docker deploy by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#525](https://github.com/fastapi-practices/fastapi_best_architecture/pull/525)
* Add async attrs for sqla mapped base by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#528](https://github.com/fastapi-practices/fastapi_best_architecture/pull/528)
* Add sqlalchemy connection pool config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#529](https://github.com/fastapi-practices/fastapi_best_architecture/pull/529)
* Fix the sql script for init data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#530](https://github.com/fastapi-practices/fastapi_best_architecture/pull/530)
* Optimize Dockerfile for faster builds by [@huyuwei1996](https://github.com/huyuwei1996) in [fastapi-practices/fastapi_best_architecture#526](https://github.com/fastapi-practices/fastapi_best_architecture/pull/526)

## New Contributors
* [@huyuwei1996](https://github.com/huyuwei1996) made their first contribution in [fastapi-practices/fastapi_best_architecture#525](https://github.com/fastapi-practices/fastapi_best_architecture/pull/525)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/compare/v1.0.0...v1.0.1

## Contributors

<a href="https://github.com/huyuwei1996"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fhuyuwei1996.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@huyuwei1996"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>

[Changes][v1.0.1]


<a id="v1.0.0"></a>
# [v1.0.0](https://github.com/fastapi-practices/fastapi-best-architecture/releases/tag/v1.0.0) - 2025-02-24

## What's Changed
* add base code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#12](https://github.com/fastapi-practices/fastapi_best_architecture/pull/12)
* fix get_user_info func return None [#9](https://github.com/fastapi-practices/fastapi-best-architecture/issues/9) by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#14](https://github.com/fastapi-practices/fastapi_best_architecture/pull/14)
* simplify user apis [#11](https://github.com/fastapi-practices/fastapi-best-architecture/issues/11) by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#18](https://github.com/fastapi-practices/fastapi_best_architecture/pull/18)
* Add environment variable management and fix Pydantic validation error by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#15](https://github.com/fastapi-practices/fastapi_best_architecture/pull/15)
* update the ruff rules and format the code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#24](https://github.com/fastapi-practices/fastapi_best_architecture/pull/24)
* improving project configuration by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#25](https://github.com/fastapi-practices/fastapi_best_architecture/pull/25)
* update to python3.10 by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#29](https://github.com/fastapi-practices/fastapi_best_architecture/pull/29)
* update Dockerfile and docker-compose.yml by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#31](https://github.com/fastapi-practices/fastapi_best_architecture/pull/31)
* Update the sub routers setting in the subdirectory by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#32](https://github.com/fastapi-practices/fastapi_best_architecture/pull/32)
* add the get project config api by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#33](https://github.com/fastapi-practices/fastapi_best_architecture/pull/33)
* add test code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#37](https://github.com/fastapi-practices/fastapi_best_architecture/pull/37)
* fix that the data validation global exception handler does not work by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#40](https://github.com/fastapi-practices/fastapi_best_architecture/pull/40)
* Fix the swagger form login structure abnormality by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#46](https://github.com/fastapi-practices/fastapi_best_architecture/pull/46)
* Bump starlette from 0.26.1 to 0.27.0 by [@dependabot](https://github.com/dependabot) in [fastapi-practices/fastapi_best_architecture#48](https://github.com/fastapi-practices/fastapi_best_architecture/pull/48)
* add rbac authorization by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#41](https://github.com/fastapi-practices/fastapi_best_architecture/pull/41)
* Bump fastapi from 0.95.0 to 0.95.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#53](https://github.com/fastapi-practices/fastapi_best_architecture/pull/53)
* Update the uniform return method to success by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#55](https://github.com/fastapi-practices/fastapi_best_architecture/pull/55)
* add token storage and logout by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#57](https://github.com/fastapi-practices/fastapi_best_architecture/pull/57)
* fix jwt parameter parsing error by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#61](https://github.com/fastapi-practices/fastapi_best_architecture/pull/61)
* add token refreshing mechanism by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#62](https://github.com/fastapi-practices/fastapi_best_architecture/pull/62)
* Update uniform return to custom encoder by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#60](https://github.com/fastapi-practices/fastapi_best_architecture/pull/60)
* update token default exception return message by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#65](https://github.com/fastapi-practices/fastapi_best_architecture/pull/65)
* add English and Chinese README jump links by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#66](https://github.com/fastapi-practices/fastapi_best_architecture/pull/66)
* update token refresh expire time rule by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#67](https://github.com/fastapi-practices/fastapi_best_architecture/pull/67)
* update the casbin to asynchronous by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#69](https://github.com/fastapi-practices/fastapi_best_architecture/pull/69)
* Update tests structure. by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#68](https://github.com/fastapi-practices/fastapi_best_architecture/pull/68)
* Add apis rate limiter by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#72](https://github.com/fastapi-practices/fastapi_best_architecture/pull/72)
* add tests exclusion E402 rule by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#73](https://github.com/fastapi-practices/fastapi_best_architecture/pull/73)
* update where query by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#74](https://github.com/fastapi-practices/fastapi_best_architecture/pull/74)
* simplify crud method naming by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#75](https://github.com/fastapi-practices/fastapi_best_architecture/pull/75)
* add login logs by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#76](https://github.com/fastapi-practices/fastapi_best_architecture/pull/76)
* add different log files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#77](https://github.com/fastapi-practices/fastapi_best_architecture/pull/77)
* add offline ip location resolution by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#78](https://github.com/fastapi-practices/fastapi_best_architecture/pull/78)
* add api module Interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#79](https://github.com/fastapi-practices/fastapi_best_architecture/pull/79)
* update token handling logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#83](https://github.com/fastapi-practices/fastapi_best_architecture/pull/83)
* add jwt authentication middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#84](https://github.com/fastapi-practices/fastapi_best_architecture/pull/84)
* Fix background task not executed by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#86](https://github.com/fastapi-practices/fastapi_best_architecture/pull/86)
* Fix the merge issues by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#87](https://github.com/fastapi-practices/fastapi_best_architecture/pull/87)
* Update docker one-click deployment by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#88](https://github.com/fastapi-practices/fastapi_best_architecture/pull/88)
* Add role-related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#89](https://github.com/fastapi-practices/fastapi_best_architecture/pull/89)
* Bump cryptography from 39.0.1 to 41.0.0 by [@dependabot](https://github.com/dependabot) in [fastapi-practices/fastapi_best_architecture#90](https://github.com/fastapi-practices/fastapi_best_architecture/pull/90)
* Add assertion error handler. by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#93](https://github.com/fastapi-practices/fastapi_best_architecture/pull/93)
* Add operation log related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#92](https://github.com/fastapi-practices/fastapi_best_architecture/pull/92)
* Fix user authorization lock by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#94](https://github.com/fastapi-practices/fastapi_best_architecture/pull/94)
* Fix the opera log cost_time parameter by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#95](https://github.com/fastapi-practices/fastapi_best_architecture/pull/95)
* Add os and browser parameters to opera log by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#97](https://github.com/fastapi-practices/fastapi_best_architecture/pull/97)
* Uniform schema class naming convention style. by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#98](https://github.com/fastapi-practices/fastapi_best_architecture/pull/98)
* Add sync to async decorator support by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#96](https://github.com/fastapi-practices/fastapi_best_architecture/pull/96)
* Add department-related interfaces and others by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#101](https://github.com/fastapi-practices/fastapi_best_architecture/pull/101)
* Remove useless jwt role_ids by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#103](https://github.com/fastapi-practices/fastapi_best_architecture/pull/103)
* Add departmental status authentication by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#104](https://github.com/fastapi-practices/fastapi_best_architecture/pull/104)
* Add casbine-related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#107](https://github.com/fastapi-practices/fastapi_best_architecture/pull/107)
* Replace aioredis to redis. by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#108](https://github.com/fastapi-practices/fastapi_best_architecture/pull/108)
* opera_log_middleware method split by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#105](https://github.com/fastapi-practices/fastapi_best_architecture/pull/105)
* Fix offline parse ip info by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#112](https://github.com/fastapi-practices/fastapi_best_architecture/pull/112)
* Update the README document by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#113](https://github.com/fastapi-practices/fastapi_best_architecture/pull/113)
* Update development process suggestions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#114](https://github.com/fastapi-practices/fastapi_best_architecture/pull/114)
* Fix log table msg field length by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#117](https://github.com/fastapi-practices/fastapi_best_architecture/pull/117)
* Add menu-related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#118](https://github.com/fastapi-practices/fastapi_best_architecture/pull/118)
* Omitting table names from the autogenerate process by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#125](https://github.com/fastapi-practices/fastapi_best_architecture/pull/125)
* Add login graphic captcha by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#124](https://github.com/fastapi-practices/fastapi_best_architecture/pull/124)
* fix the operation log storage exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#130](https://github.com/fastapi-practices/fastapi_best_architecture/pull/130)
* add dictionary management interface by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#127](https://github.com/fastapi-practices/fastapi_best_architecture/pull/127)
* Update and fix permissions logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#129](https://github.com/fastapi-practices/fastapi_best_architecture/pull/129)
* Update JWT status detection by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#133](https://github.com/fastapi-practices/fastapi_best_architecture/pull/133)
* The level field is deprecated but remained by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#134](https://github.com/fastapi-practices/fastapi_best_architecture/pull/134)
* Add system monitoring interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#135](https://github.com/fastapi-practices/fastapi_best_architecture/pull/135)
* Fix the operation log message error by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#140](https://github.com/fastapi-practices/fastapi_best_architecture/pull/140)
* Update the server monitoring interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#141](https://github.com/fastapi-practices/fastapi_best_architecture/pull/141)
* Update the status field type to int by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#143](https://github.com/fastapi-practices/fastapi_best_architecture/pull/143)
* Fix the operation log field type error by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#145](https://github.com/fastapi-practices/fastapi_best_architecture/pull/145)
* Fix the exception handler HTTPException type error by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#146](https://github.com/fastapi-practices/fastapi_best_architecture/pull/146)
* Add the schema base class by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#148](https://github.com/fastapi-practices/fastapi_best_architecture/pull/148)
* Add datetime util by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#149](https://github.com/fastapi-practices/fastapi_best_architecture/pull/149)
* Fix permitted exception. by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#151](https://github.com/fastapi-practices/fastapi_best_architecture/pull/151)
* Refactor global datetime to timezone datetime by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#152](https://github.com/fastapi-practices/fastapi_best_architecture/pull/152)
* Add processing after password reset by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#154](https://github.com/fastapi-practices/fastapi_best_architecture/pull/154)
* Update some routing groups by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#155](https://github.com/fastapi-practices/fastapi_best_architecture/pull/155)
* Add task-related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#157](https://github.com/fastapi-practices/fastapi_best_architecture/pull/157)
* Update the instructions in the readme by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#159](https://github.com/fastapi-practices/fastapi_best_architecture/pull/159)
* Update some interface permission checks by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#158](https://github.com/fastapi-practices/fastapi_best_architecture/pull/158)
* Add database init sql files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#160](https://github.com/fastapi-practices/fastapi_best_architecture/pull/160)
* Adapt to frontend by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#162](https://github.com/fastapi-practices/fastapi_best_architecture/pull/162)
* Update menu handling logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#163](https://github.com/fastapi-practices/fastapi_best_architecture/pull/163)
* Bump fastapi from 0.95.2 to 0.99.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#164](https://github.com/fastapi-practices/fastapi_best_architecture/pull/164)
* Enable login interface captcha function by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#165](https://github.com/fastapi-practices/fastapi_best_architecture/pull/165)
* Fix CORS 500 status code exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#167](https://github.com/fastapi-practices/fastapi_best_architecture/pull/167)
* Add menu table title field by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#170](https://github.com/fastapi-practices/fastapi_best_architecture/pull/170)
* fix tree data algorithms exception by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#169](https://github.com/fastapi-practices/fastapi_best_architecture/pull/169)
* Fix the menu query children exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#171](https://github.com/fastapi-practices/fastapi_best_architecture/pull/171)
* Custom request rate limit callback function by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#174](https://github.com/fastapi-practices/fastapi_best_architecture/pull/174)
* Add demo site mode by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#173](https://github.com/fastapi-practices/fastapi_best_architecture/pull/173)
* Add query users by department ID by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#175](https://github.com/fastapi-practices/fastapi_best_architecture/pull/175)
* Update monitoring return data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#176](https://github.com/fastapi-practices/fastapi_best_architecture/pull/176)
* Update user role interface to standalone by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#177](https://github.com/fastapi-practices/fastapi_best_architecture/pull/177)
* Add get roles related interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#178](https://github.com/fastapi-practices/fastapi_best_architecture/pull/178)
* Add the role status conditional query by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#181](https://github.com/fastapi-practices/fastapi_best_architecture/pull/181)
* Update role menu interface is standalone by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#182](https://github.com/fastapi-practices/fastapi_best_architecture/pull/182)
* Add interface to get all menus of a role by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#183](https://github.com/fastapi-practices/fastapi_best_architecture/pull/183)
* Fix schema enum condition exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#185](https://github.com/fastapi-practices/fastapi_best_architecture/pull/185)
* Bump Async SQLAlchemy Adapter from 1.1.0 to 1.2.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#187](https://github.com/fastapi-practices/fastapi_best_architecture/pull/187)
* Bump cryptography from 41.0.0 to 41.0.2 by [@dependabot](https://github.com/dependabot) in [fastapi-practices/fastapi_best_architecture#179](https://github.com/fastapi-practices/fastapi_best_architecture/pull/179)
* Update SQL files and use them as execution targets by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#188](https://github.com/fastapi-practices/fastapi_best_architecture/pull/188)
* Add user password encryption salt by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#191](https://github.com/fastapi-practices/fastapi_best_architecture/pull/191)
* Update roles and nickname fields to be optiona by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#190](https://github.com/fastapi-practices/fastapi_best_architecture/pull/190)
* Fix casbin async enforcer by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#192](https://github.com/fastapi-practices/fastapi_best_architecture/pull/192)
* Add more Casbin related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#195](https://github.com/fastapi-practices/fastapi_best_architecture/pull/195)
* Update the nickname field creation logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#196](https://github.com/fastapi-practices/fastapi_best_architecture/pull/196)
* Update the Casbin model matcher rules by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#197](https://github.com/fastapi-practices/fastapi_best_architecture/pull/197)
* Add api and casbin related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#198](https://github.com/fastapi-practices/fastapi_best_architecture/pull/198)
* Update asynccasbin to casbin async api by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#199](https://github.com/fastapi-practices/fastapi_best_architecture/pull/199)
* Fix the interface logic for dept details by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#201](https://github.com/fastapi-practices/fastapi_best_architecture/pull/201)
* Add ItsDangerous request parameters encryption by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#203](https://github.com/fastapi-practices/fastapi_best_architecture/pull/203)
* Add jwt login whitelist by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#204](https://github.com/fastapi-practices/fastapi_best_architecture/pull/204)
* Add ip location cache by [@downdawn](https://github.com/downdawn) in [fastapi-practices/fastapi_best_architecture#205](https://github.com/fastapi-practices/fastapi_best_architecture/pull/205)
* Fix int enum class inheritance by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#208](https://github.com/fastapi-practices/fastapi_best_architecture/pull/208)
* Fix the task interface return data by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#215](https://github.com/fastapi-practices/fastapi_best_architecture/pull/215)
* Update the README document by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#214](https://github.com/fastapi-practices/fastapi_best_architecture/pull/214)
* Fix token whitelist and new token storage by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#220](https://github.com/fastapi-practices/fastapi_best_architecture/pull/220)
* Optimize role menu authorization logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#221](https://github.com/fastapi-practices/fastapi_best_architecture/pull/221)
* Simplified query interface returns data serialization by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#219](https://github.com/fastapi-practices/fastapi_best_architecture/pull/219)
* Update the global unified response code by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#223](https://github.com/fastapi-practices/fastapi_best_architecture/pull/223)
* Fix global unknown exception return by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#224](https://github.com/fastapi-practices/fastapi_best_architecture/pull/224)
* Update the pytz library to zoneinfo by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#226](https://github.com/fastapi-practices/fastapi_best_architecture/pull/226)
* Add token decoding expiration exception by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#227](https://github.com/fastapi-practices/fastapi_best_architecture/pull/227)
* Fix the task run method and data type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#228](https://github.com/fastapi-practices/fastapi_best_architecture/pull/228)
* Remove the NoReturn return type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#232](https://github.com/fastapi-practices/fastapi_best_architecture/pull/232)
* Add init pytest data sql file by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#231](https://github.com/fastapi-practices/fastapi_best_architecture/pull/231)
* Fix pytest interface unit tests by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#233](https://github.com/fastapi-practices/fastapi_best_architecture/pull/233)
* Replace APScheduler to Celery asynchronous tasks by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#229](https://github.com/fastapi-practices/fastapi_best_architecture/pull/229)
* Fix the conflict between Access and OperaLog middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#236](https://github.com/fastapi-practices/fastapi_best_architecture/pull/236)
* Fix unregistered error received when celery call task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#239](https://github.com/fastapi-practices/fastapi_best_architecture/pull/239)
* Fix database engine UUID type compatibility by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#241](https://github.com/fastapi-practices/fastapi_best_architecture/pull/241)
* adopt ruff formatter by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#242](https://github.com/fastapi-practices/fastapi_best_architecture/pull/242)
* Bump cryptography from 41.0.2 to 41.0.6 by [@dependabot](https://github.com/dependabot) in [fastapi-practices/fastapi_best_architecture#243](https://github.com/fastapi-practices/fastapi_best_architecture/pull/243)
* Add a telegram interactive link by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#245](https://github.com/fastapi-practices/fastapi_best_architecture/pull/245)
* Fix validation error log code return type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#247](https://github.com/fastapi-practices/fastapi_best_architecture/pull/247)
* Fix refresh token interface user type format by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#248](https://github.com/fastapi-practices/fastapi_best_architecture/pull/248)
* Optimize operation log code type logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#249](https://github.com/fastapi-practices/fastapi_best_architecture/pull/249)
* Fix get all G rules interface logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#250](https://github.com/fastapi-practices/fastapi_best_architecture/pull/250)
* Simplify the multivariate expression of exceptions handler by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#252](https://github.com/fastapi-practices/fastapi_best_architecture/pull/252)
* Fix exception handler parameter call by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#253](https://github.com/fastapi-practices/fastapi_best_architecture/pull/253)
* Prepare to lock the pydantic-v1 branch by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#254](https://github.com/fastapi-practices/fastapi_best_architecture/pull/254)
* Add a stand-alone assertion error handler by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#255](https://github.com/fastapi-practices/fastapi_best_architecture/pull/255)
* Clean up todo and fix typo by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#256](https://github.com/fastapi-practices/fastapi_best_architecture/pull/256)
* Migrate to pydantic-v2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#246](https://github.com/fastapi-practices/fastapi_best_architecture/pull/246)
* Add pydantic-v2 migration reminder by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#257](https://github.com/fastapi-practices/fastapi_best_architecture/pull/257)
* Add the project status page to the README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#259](https://github.com/fastapi-practices/fastapi_best_architecture/pull/259)
* Clean up outdated pydantic dict methods by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#262](https://github.com/fastapi-practices/fastapi_best_architecture/pull/262)
* Fix use request.form() in middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#260](https://github.com/fastapi-practices/fastapi_best_architecture/pull/260)
* Reconstruct RBAC authentication logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#264](https://github.com/fastapi-practices/fastapi_best_architecture/pull/264)
* Attempt to optimize serialization performance by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#266](https://github.com/fastapi-practices/fastapi_best_architecture/pull/266)
* Update schemas naming style by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#272](https://github.com/fastapi-practices/fastapi_best_architecture/pull/272)
* Update sponsor links and FUNDING by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#273](https://github.com/fastapi-practices/fastapi_best_architecture/pull/273)
* Fix dept and menu parent id update logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#274](https://github.com/fastapi-practices/fastapi_best_architecture/pull/274)
* Update interface coding style by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#275](https://github.com/fastapi-practices/fastapi_best_architecture/pull/275)
* Update dao and service instantiation styles by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#276](https://github.com/fastapi-practices/fastapi_best_architecture/pull/276)
* Add custom email string type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#277](https://github.com/fastapi-practices/fastapi_best_architecture/pull/277)
* Fix custom validator exception serialization in dev mode by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#278](https://github.com/fastapi-practices/fastapi_best_architecture/pull/278)
* Restore the Github ci workflows by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#281](https://github.com/fastapi-practices/fastapi_best_architecture/pull/281)
* Add the pdm project manager by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#282](https://github.com/fastapi-practices/fastapi_best_architecture/pull/282)
* Add the front-end docker-compose script by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#283](https://github.com/fastapi-practices/fastapi_best_architecture/pull/283)
* Update the response status code in exception handlers by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#292](https://github.com/fastapi-practices/fastapi_best_architecture/pull/292)
* Update interface file directory level by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#295](https://github.com/fastapi-practices/fastapi_best_architecture/pull/295)
* Add the repository star map by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#296](https://github.com/fastapi-practices/fastapi_best_architecture/pull/296)
* Add OAuth 2.0 authorization login by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#293](https://github.com/fastapi-practices/fastapi_best_architecture/pull/293)
* Prepare to lock the legacy branch by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#301](https://github.com/fastapi-practices/fastapi_best_architecture/pull/301)
* Update the README.md branch prompt by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#302](https://github.com/fastapi-practices/fastapi_best_architecture/pull/302)
* Refactor the backend architecture by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#299](https://github.com/fastapi-practices/fastapi_best_architecture/pull/299)
* Fix English README.md update date by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#308](https://github.com/fastapi-practices/fastapi_best_architecture/pull/308)
* Add backend scripts description by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#309](https://github.com/fastapi-practices/fastapi_best_architecture/pull/309)
* Fix missing data from alembic migration by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#312](https://github.com/fastapi-practices/fastapi_best_architecture/pull/312)
* Update CRUDBase to sqlalchemy-crud-plus by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#317](https://github.com/fastapi-practices/fastapi_best_architecture/pull/317)
* Upgrade and update fastapi service startup by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#319](https://github.com/fastapi-practices/fastapi_best_architecture/pull/319)
* Delete the gzip middleware to improve performance by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#325](https://github.com/fastapi-practices/fastapi_best_architecture/pull/325)
* Add interface fast response method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#327](https://github.com/fastapi-practices/fastapi_best_architecture/pull/327)
* Update the opera log middleware task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#326](https://github.com/fastapi-practices/fastapi_best_architecture/pull/326)
* Add test account to README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#330](https://github.com/fastapi-practices/fastapi_best_architecture/pull/330)
* Restore the main startup of fastapi service by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#336](https://github.com/fastapi-practices/fastapi_best_architecture/pull/336)
* Update app route definition rules by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#341](https://github.com/fastapi-practices/fastapi_best_architecture/pull/341)
* Add Linux Do OAuth2 login by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#343](https://github.com/fastapi-practices/fastapi_best_architecture/pull/343)
* Fix user social binding query by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#344](https://github.com/fastapi-practices/fastapi_best_architecture/pull/344)
* Refactor global log default handler by [@obrua](https://github.com/obrua) in [fastapi-practices/fastapi_best_architecture#347](https://github.com/fastapi-practices/fastapi_best_architecture/pull/347)
* Add code generator app by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#318](https://github.com/fastapi-practices/fastapi_best_architecture/pull/318)
* Update and enable access log middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#348](https://github.com/fastapi-practices/fastapi_best_architecture/pull/348)
* Add code generator README document by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#349](https://github.com/fastapi-practices/fastapi_best_architecture/pull/349)
* Fix model template conditional syntax by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#351](https://github.com/fastapi-practices/fastapi_best_architecture/pull/351)
* Update code generation model column type storage by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#352](https://github.com/fastapi-practices/fastapi_best_architecture/pull/352)
* Fix gen model and schema template formatting by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#356](https://github.com/fastapi-practices/fastapi_best_architecture/pull/356)
* Add code generator to create init files by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#358](https://github.com/fastapi-practices/fastapi_best_architecture/pull/358)
* Fix alembic migration failure caused by model by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#359](https://github.com/fastapi-practices/fastapi_best_architecture/pull/359)
* Update the docker-compose deployment script by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#360](https://github.com/fastapi-practices/fastapi_best_architecture/pull/360)
* Update oauth2 route naming and return by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#361](https://github.com/fastapi-practices/fastapi_best_architecture/pull/361)
* Bump fast captcha version to 0.3.2 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#362](https://github.com/fastapi-practices/fastapi_best_architecture/pull/362)
* Update crud user staff field logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#363](https://github.com/fastapi-practices/fastapi_best_architecture/pull/363)
* Fix code auto-generated model creation by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#364](https://github.com/fastapi-practices/fastapi_best_architecture/pull/364)
* Add page to display dynamic configuration by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#365](https://github.com/fastapi-practices/fastapi_best_architecture/pull/365)
* Fix celery asynchronous task execution by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#367](https://github.com/fastapi-practices/fastapi_best_architecture/pull/367)
* Update operation log middleware info reading by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#368](https://github.com/fastapi-practices/fastapi_best_architecture/pull/368)
* Update create new token function return type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#369](https://github.com/fastapi-practices/fastapi_best_architecture/pull/369)
* Update access log cost time style by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#370](https://github.com/fastapi-practices/fastapi_best_architecture/pull/370)
* Update code generate business model time column by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#371](https://github.com/fastapi-practices/fastapi_best_architecture/pull/371)
* Add custom code template pathname config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#372](https://github.com/fastapi-practices/fastapi_best_architecture/pull/372)
* Update some code generation api and params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#373](https://github.com/fastapi-practices/fastapi_best_architecture/pull/373)
* Update code generate download api auth by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#376](https://github.com/fastapi-practices/fastapi_best_architecture/pull/376)
* Update current menu status auth by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#374](https://github.com/fastapi-practices/fastapi_best_architecture/pull/374)
* Fix code generation model create and update by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#378](https://github.com/fastapi-practices/fastapi_best_architecture/pull/378)
* Update user and auth error message by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#379](https://github.com/fastapi-practices/fastapi_best_architecture/pull/379)
* Add directory tree and update app notes by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#380](https://github.com/fastapi-practices/fastapi_best_architecture/pull/380)
* Optimize serialization and jwt performance by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#382](https://github.com/fastapi-practices/fastapi_best_architecture/pull/382)
* Fix arm system cpu frequency retrieval by [@yshan2028](https://github.com/yshan2028) in [fastapi-practices/fastapi_best_architecture#385](https://github.com/fastapi-practices/fastapi_best_architecture/pull/385)
* Fix logging when a login error occurs by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#386](https://github.com/fastapi-practices/fastapi_best_architecture/pull/386)
* Update redis cache prefix separator to `:` by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#387](https://github.com/fastapi-practices/fastapi_best_architecture/pull/387)
* Bump sqlalchemy crud plus version to 1.3.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#388](https://github.com/fastapi-practices/fastapi_best_architecture/pull/388)
* Update the README announcement to note by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#390](https://github.com/fastapi-practices/fastapi_best_architecture/pull/390)
* Fix code generation to new features by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#393](https://github.com/fastapi-practices/fastapi_best_architecture/pull/393)
* Fix OAuth2 user query conditions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#396](https://github.com/fastapi-practices/fastapi_best_architecture/pull/396)
* Fix the user permissions update services by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#397](https://github.com/fastapi-practices/fastapi_best_architecture/pull/397)
* Update code generate comment column format by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#399](https://github.com/fastapi-practices/fastapi_best_architecture/pull/399)
* Update the interactive link address by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#402](https://github.com/fastapi-practices/fastapi_best_architecture/pull/402)
* Updated refresh token storage logic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#403](https://github.com/fastapi-practices/fastapi_best_architecture/pull/403)
* Fix server monitor io blocking by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#404](https://github.com/fastapi-practices/fastapi_best_architecture/pull/404)
* Fix cookie expiration time zone by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#408](https://github.com/fastapi-practices/fastapi_best_architecture/pull/408)
* Add request trace ID record by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#409](https://github.com/fastapi-practices/fastapi_best_architecture/pull/409)
* Optimize the naming of setting params by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#410](https://github.com/fastapi-practices/fastapi_best_architecture/pull/410)
* Add trace ID to exception handlers by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#411](https://github.com/fastapi-practices/fastapi_best_architecture/pull/411)
* Update the global exception log stack by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#406](https://github.com/fastapi-practices/fastapi_best_architecture/pull/406)
* Bump pydantic from 2.8.1 to 2.9.1 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#412](https://github.com/fastapi-practices/fastapi_best_architecture/pull/412)
* Optimize exception info opera log record by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#413](https://github.com/fastapi-practices/fastapi_best_architecture/pull/413)
* Fix log output and logging levels by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#414](https://github.com/fastapi-practices/fastapi_best_architecture/pull/414)
* Fix exception logging in opera log by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#417](https://github.com/fastapi-practices/fastapi_best_architecture/pull/417)
* Fix the gen model template formatting by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#416](https://github.com/fastapi-practices/fastapi_best_architecture/pull/416)
* Optimize the internal implementation of serializers by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#419](https://github.com/fastapi-practices/fastapi_best_architecture/pull/419)
* Fix for create new token cache delete by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#420](https://github.com/fastapi-practices/fastapi_best_architecture/pull/420)
* Update JWT errors class import by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#421](https://github.com/fastapi-practices/fastapi_best_architecture/pull/421)
* Update multi login sync update refresh tokens by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#422](https://github.com/fastapi-practices/fastapi_best_architecture/pull/422)
* Update sync function calls in JWT by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#423](https://github.com/fastapi-practices/fastapi_best_architecture/pull/423)
* Fix the missing OAuth2 interface parameters by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#425](https://github.com/fastapi-practices/fastapi_best_architecture/pull/425)
* Add request state middleware by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#426](https://github.com/fastapi-practices/fastapi_best_architecture/pull/426)
* Fix pydantic field and model validator by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#427](https://github.com/fastapi-practices/fastapi_best_architecture/pull/427)
* Fix the OAuth2 service login log task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#428](https://github.com/fastapi-practices/fastapi_best_architecture/pull/428)
* Update official documentation link to README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#429](https://github.com/fastapi-practices/fastapi_best_architecture/pull/429)
* Optimize and normalize the code generator by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#430](https://github.com/fastapi-practices/fastapi_best_architecture/pull/430)
* Bump redis from 5.0.1 to 5.1.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#433](https://github.com/fastapi-practices/fastapi_best_architecture/pull/433)
* Update interactive link descriptions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#434](https://github.com/fastapi-practices/fastapi_best_architecture/pull/434)
* Optimize the serialize return of SQLA select by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#436](https://github.com/fastapi-practices/fastapi_best_architecture/pull/436)
* Update project manager pdm to uv by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#440](https://github.com/fastapi-practices/fastapi_best_architecture/pull/440)
* Add asynchronous socketio application server by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#437](https://github.com/fastapi-practices/fastapi_best_architecture/pull/437)
* Add dependency-groups by PEP 735 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#444](https://github.com/fastapi-practices/fastapi_best_architecture/pull/444)
* Update the usage documentation in README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#449](https://github.com/fastapi-practices/fastapi_best_architecture/pull/449)
* Bump sqlalchemy crud plus version to 1.5.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#450](https://github.com/fastapi-practices/fastapi_best_architecture/pull/450)
* Update singleton pattern class typing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#452](https://github.com/fastapi-practices/fastapi_best_architecture/pull/452)
* Update system config to be dynamic by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#447](https://github.com/fastapi-practices/fastapi_best_architecture/pull/447)
* Update multiple version dependency specifiers by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#454](https://github.com/fastapi-practices/fastapi_best_architecture/pull/454)
* Fix typo in contribution description by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#456](https://github.com/fastapi-practices/fastapi_best_architecture/pull/456)
* Fix code generation file missing by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#457](https://github.com/fastapi-practices/fastapi_best_architecture/pull/457)
* Update the celery configuration and tasks by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#458](https://github.com/fastapi-practices/fastapi_best_architecture/pull/458)
* Update some service class invocations by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#459](https://github.com/fastapi-practices/fastapi_best_architecture/pull/459)
* Update code generator API file structure by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#460](https://github.com/fastapi-practices/fastapi_best_architecture/pull/460)
* Update api body params to schema by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#461](https://github.com/fastapi-practices/fastapi_best_architecture/pull/461)
* Fix celery service functions error by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#462](https://github.com/fastapi-practices/fastapi_best_architecture/pull/462)
* Update user password encryption method by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#463](https://github.com/fastapi-practices/fastapi_best_architecture/pull/463)
* Update role-based data permissions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#465](https://github.com/fastapi-practices/fastapi_best_architecture/pull/465)
* Bump tornado from 6.4.1 to 6.4.2 in /backend by [@dependabot](https://github.com/dependabot) in [fastapi-practices/fastapi_best_architecture#466](https://github.com/fastapi-practices/fastapi_best_architecture/pull/466)
* Fix schema type of user role rule by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#467](https://github.com/fastapi-practices/fastapi_best_architecture/pull/467)
* Simplify data rule and remove type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#468](https://github.com/fastapi-practices/fastapi_best_architecture/pull/468)
* Add the project logo to README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#469](https://github.com/fastapi-practices/fastapi_best_architecture/pull/469)
* Optimized user auth for auth service by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#472](https://github.com/fastapi-practices/fastapi_best_architecture/pull/472)
* Fix data rule expression column comment by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#473](https://github.com/fastapi-practices/fastapi_best_architecture/pull/473)
* Fix and update alembic env and ini by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#474](https://github.com/fastapi-practices/fastapi_best_architecture/pull/474)
* Fix login log parameter error in task by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#476](https://github.com/fastapi-practices/fastapi_best_architecture/pull/476)
* Remove data scope in the role model by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#478](https://github.com/fastapi-practices/fastapi_best_architecture/pull/478)
* Add postgresql database support by [@Meepoljdx](https://github.com/Meepoljdx) in [fastapi-practices/fastapi_best_architecture#475](https://github.com/fastapi-practices/fastapi_best_architecture/pull/475)
* Update opera log cost time precision by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#479](https://github.com/fastapi-practices/fastapi_best_architecture/pull/479)
* Update opera middleware request args parse by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#481](https://github.com/fastapi-practices/fastapi_best_architecture/pull/481)
* Bump msgspec from 0.18.6 to 0.19.0 by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#482](https://github.com/fastapi-practices/fastapi_best_architecture/pull/482)
* Fix user cache when updated user role by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#483](https://github.com/fastapi-practices/fastapi_best_architecture/pull/483)
* Update the route version define location by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#485](https://github.com/fastapi-practices/fastapi_best_architecture/pull/485)
* Optimize docker deploy settings and scripts by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#486](https://github.com/fastapi-practices/fastapi_best_architecture/pull/486)
* Add system notice interface by [@dividduang](https://github.com/dividduang) in [fastapi-practices/fastapi_best_architecture#487](https://github.com/fastapi-practices/fastapi_best_architecture/pull/487)
* Add response model include data schema by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#490](https://github.com/fastapi-practices/fastapi_best_architecture/pull/490)
* Update redocs arg and url to redoc by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#493](https://github.com/fastapi-practices/fastapi_best_architecture/pull/493)
* Fix serialization when pagination is empty by [@qhp13654398483](https://github.com/qhp13654398483) in [fastapi-practices/fastapi_best_architecture#491](https://github.com/fastapi-practices/fastapi_best_architecture/pull/491)
* Update return schema of query interface by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#492](https://github.com/fastapi-practices/fastapi_best_architecture/pull/492)
* Add token related interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#495](https://github.com/fastapi-practices/fastapi_best_architecture/pull/495)
* Fix return schema of user me api by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#497](https://github.com/fastapi-practices/fastapi_best_architecture/pull/497)
* Fix current user info detail schema by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#499](https://github.com/fastapi-practices/fastapi_best_architecture/pull/499)
* Update menu field show to display by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#498](https://github.com/fastapi-practices/fastapi_best_architecture/pull/498)
* Fix casbin policy api return schema by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#500](https://github.com/fastapi-practices/fastapi_best_architecture/pull/500)
* Fix opera log of non-dict request body by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#501](https://github.com/fastapi-practices/fastapi_best_architecture/pull/501)
* Bump dependencies and pre-commits by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#504](https://github.com/fastapi-practices/fastapi_best_architecture/pull/504)
* Fix the return datetime data encoder by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#505](https://github.com/fastapi-practices/fastapi_best_architecture/pull/505)
* Fix fastapi config variable naming and type by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#506](https://github.com/fastapi-practices/fastapi_best_architecture/pull/506)
* Fix the user pagination api return schema by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#507](https://github.com/fastapi-practices/fastapi_best_architecture/pull/507)
* Fix OAuth2 service register user args by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#508](https://github.com/fastapi-practices/fastapi_best_architecture/pull/508)
* Fix OAuth2 service user last login time by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#509](https://github.com/fastapi-practices/fastapi_best_architecture/pull/509)
* Fix OAuth2 service user last login time by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#510](https://github.com/fastapi-practices/fastapi_best_architecture/pull/510)
* Add plugin system and notice plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#503](https://github.com/fastapi-practices/fastapi_best_architecture/pull/503)
* Delete the threads in gunicorn config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#512](https://github.com/fastapi-practices/fastapi_best_architecture/pull/512)
* Add plugin requirements auto install functions by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#514](https://github.com/fastapi-practices/fastapi_best_architecture/pull/514)
* Update casbin rbac verify to plugin by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#513](https://github.com/fastapi-practices/fastapi_best_architecture/pull/513)
* Update the logic for create new token by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#516](https://github.com/fastapi-practices/fastapi_best_architecture/pull/516)
* Add local file upload interfaces by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#489](https://github.com/fastapi-practices/fastapi_best_architecture/pull/489)
* Update loguru and deploy log config by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#517](https://github.com/fastapi-practices/fastapi_best_architecture/pull/517)
* Delete the model redundancy level field by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#518](https://github.com/fastapi-practices/fastapi_best_architecture/pull/518)
* Update the built-in features in README by [@wu-clan](https://github.com/wu-clan) in [fastapi-practices/fastapi_best_architecture#519](https://github.com/fastapi-practices/fastapi_best_architecture/pull/519)

## New Contributors
* [@downdawn](https://github.com/downdawn) made their first contribution in [fastapi-practices/fastapi_best_architecture#15](https://github.com/fastapi-practices/fastapi_best_architecture/pull/15)
* [@dependabot](https://github.com/dependabot) made their first contribution in [fastapi-practices/fastapi_best_architecture#48](https://github.com/fastapi-practices/fastapi_best_architecture/pull/48)
* [@obrua](https://github.com/obrua) made their first contribution in [fastapi-practices/fastapi_best_architecture#347](https://github.com/fastapi-practices/fastapi_best_architecture/pull/347)
* [@yshan2028](https://github.com/yshan2028) made their first contribution in [fastapi-practices/fastapi_best_architecture#385](https://github.com/fastapi-practices/fastapi_best_architecture/pull/385)
* [@Meepoljdx](https://github.com/Meepoljdx) made their first contribution in [fastapi-practices/fastapi_best_architecture#475](https://github.com/fastapi-practices/fastapi_best_architecture/pull/475)
* [@dividduang](https://github.com/dividduang) made their first contribution in [fastapi-practices/fastapi_best_architecture#487](https://github.com/fastapi-practices/fastapi_best_architecture/pull/487)
* [@qhp13654398483](https://github.com/qhp13654398483) made their first contribution in [fastapi-practices/fastapi_best_architecture#491](https://github.com/fastapi-practices/fastapi_best_architecture/pull/491)

**Full Changelog**: https://github.com/fastapi-practices/fastapi_best_architecture/commits/v1.0.0

## Contributors

<a href="https://github.com/Meepoljdx"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2FMeepoljdx.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@Meepoljdx"></a>
<a href="https://github.com/dependabot"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdependabot.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@dependabot"></a>
<a href="https://github.com/dividduang"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdividduang.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@dividduang"></a>
<a href="https://github.com/downdawn"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fdowndawn.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@downdawn"></a>
<a href="https://github.com/obrua"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fobrua.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@obrua"></a>
<a href="https://github.com/qhp13654398483"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fqhp13654398483.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@qhp13654398483"></a>
<a href="https://github.com/wu-clan"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fwu-clan.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@wu-clan"></a>
<a href="https://github.com/yshan2028"><img src="https://wsrv.nl/?url=https%3A%2F%2Fgithub.com%2Fyshan2028.png&w=128&h=128&fit=cover&mask=circle" width="64" height="64" alt="@yshan2028"></a>

[Changes][v1.0.0]


[v1.14.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.4...v1.14.0
[v1.13.4]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.3...v1.13.4
[v1.13.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.2...v1.13.3
[v1.13.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.1...v1.13.2
[v1.13.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.13.0...v1.13.1
[v1.13.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.12.3...v1.13.0
[v1.12.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.12.2...v1.12.3
[v1.12.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.12.1...v1.12.2
[v1.12.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.12.0...v1.12.1
[v1.12.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.11.2...v1.12.0
[v1.11.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.11.1...v1.11.2
[v1.11.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.11.0...v1.11.1
[v1.11.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.10.4...v1.11.0
[v1.10.4]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.10.3...v1.10.4
[v1.10.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.10.2...v1.10.3
[v1.10.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.10.1...v1.10.2
[v1.10.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.10.0...v1.10.1
[v1.10.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.9.0...v1.10.0
[v1.9.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.8.3...v1.9.0
[v1.8.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.8.2...v1.8.3
[v1.8.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.8.1...v1.8.2
[v1.8.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.8.0...v1.8.1
[v1.8.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.7.0...v1.8.0
[v1.7.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.6.0...v1.7.0
[v1.6.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.5.2...v1.6.0
[v1.5.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.5.1...v1.5.2
[v1.5.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.5.0...v1.5.1
[v1.5.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.4.3...v1.5.0
[v1.4.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.4.2...v1.4.3
[v1.4.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.4.1...v1.4.2
[v1.4.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.4.0...v1.4.1
[v1.4.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.3.0...v1.4.0
[v1.3.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.1.2...v1.2.0
[v1.1.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.1.1...v1.1.2
[v1.1.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.1.0...v1.1.1
[v1.1.0]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.5...v1.1.0
[v1.0.5]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.4...v1.0.5
[v1.0.4]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.3...v1.0.4
[v1.0.3]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.2...v1.0.3
[v1.0.2]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.1...v1.0.2
[v1.0.1]: https://github.com/fastapi-practices/fastapi-best-architecture/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/fastapi-practices/fastapi-best-architecture/tree/v1.0.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.9.1 -->
