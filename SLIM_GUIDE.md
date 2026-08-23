# FBA-Slim 瘦身指南

> 本文档记录了 fba-slim 与 fba 完整版之间的差异，方便日后从完整版合并代码时快速瘦身

## 功能差异概览

| 模块                            | 完整版 | 精简版 | 说明                          |
|-------------------------------|-----|-----|-----------------------------|
| 用户认证 (JWT)                    | ✅   | ✅   | 完整保留                        |
| RBAC (角色/菜单/部门/权限校验)          | ✅   | ❌   | 整体移除，仅保留 `DependsSuperUser` |
| 用户 CRUD                       | ✅   | ✅   | 保留（移除 dept/role 关联）         |
| 操作日志/登录日志                     | ✅   | ❌   | 移除 DB 日志，中间件仅控制台输出          |
| 多级缓存 (Local + Redis + PubSub) | ✅   | ✅   | 完整保留                        |
| Snowflake 分布式 ID              | ✅   | ✅   | 完整保留                        |
| 文件上传                          | ✅   | ✅   | 完整保留                        |
| 密码安全/历史记录                     | ✅   | ✅   | 完整保留                        |
| config 插件                     | ✅   | ✅   | 保留                          |
| 插件核心系统                        | ✅   | ✅   | 保留插件安装/卸载机制，内置仅 `config` |
| Celery 任务系统                   | ✅   | ❌   | 整体移除                        |
| Socket.IO 实时通信                | ✅   | ❌   | 整体移除                        |
| Prometheus + OTel 可观测性        | ✅   | ❌   | 整体移除                        |
| 监控 API (online/redis/server)  | ✅   | ❌   | 整体移除                        |
| 数据权限 (DataRule/DataScope)     | ✅   | ❌   | 整体移除                        |
| dict 插件                       | ✅   | ❌   | 整体移除                        |
| email 插件                      | ✅   | ❌   | 整体移除                        |
| notice 插件                     | ✅   | ❌   | 整体移除                        |
| oauth2 插件                     | ✅   | ❌   | 整体移除                        |
| code_generator 插件             | ✅   | ❌   | 整体移除                        |

## 插件范围

精简版仓库只内置 `config` 插件，`backend/plugin/` 下不得保留其他业务插件目录

- `backend/core/conf.py` 中 `PLUGIN_REQUIRED` 固定为 `['config']`
- `backend/plugin/config/` 是唯一随仓库发布的插件
- 插件核心、CLI 和插件管理 API 仍然保留，用于后续按需安装外部插件
- 不保留 AI、dict、email、notice、oauth2、code_generator 等插件及其依赖

---

## 已删除的目录

```
backend/app/task/                           # Celery 任务系统
backend/common/socketio/                    # Socket.IO 实时通信
backend/common/observability/               # Prometheus + OpenTelemetry
backend/app/admin/api/v1/monitor/           # 监控 API (online/redis/server)
backend/app/admin/tests/                    # 测试文件
backend/app/admin/api/v1/log/               # 日志 API (login_log/opera_log)
backend/plugin/dict/                        # 字典插件
backend/plugin/email/                       # 邮件插件
backend/plugin/notice/                      # 通知插件
backend/plugin/oauth2/                      # OAuth2 插件
backend/plugin/code_generator/              # 代码生成插件
backend/plugin/ai/                          # AI 插件
deploy/backend/grafana/                     # Grafana 部署配置
```

## 已删除的文件

```
# RBAC (角色/菜单/部门)
backend/app/admin/model/role.py
backend/app/admin/model/menu.py
backend/app/admin/model/dept.py
backend/app/admin/model/m2m.py
backend/app/admin/schema/role.py
backend/app/admin/schema/menu.py
backend/app/admin/schema/dept.py
backend/app/admin/crud/crud_role.py
backend/app/admin/crud/crud_menu.py
backend/app/admin/crud/crud_dept.py
backend/app/admin/service/role_service.py
backend/app/admin/service/menu_service.py
backend/app/admin/service/dept_service.py
backend/app/admin/api/v1/sys/role.py
backend/app/admin/api/v1/sys/menu.py
backend/app/admin/api/v1/sys/dept.py
backend/common/security/rbac.py
backend/common/security/permission.py
backend/utils/build_tree.py

# 数据权限
backend/app/admin/model/data_rule.py
backend/app/admin/model/data_scope.py
backend/app/admin/schema/data_rule.py
backend/app/admin/schema/data_scope.py
backend/app/admin/crud/crud_data_rule.py
backend/app/admin/crud/crud_data_scope.py
backend/app/admin/service/data_rule_service.py
backend/app/admin/service/data_scope_service.py
backend/app/admin/api/v1/sys/data_rule.py
backend/app/admin/api/v1/sys/data_scope.py

# 监控 API
backend/app/admin/schema/monitor.py

# 可观测性
backend/common/observability/otel.py
backend/common/observability/prometheus/fastapi.py
backend/common/observability/prometheus/queue.py
backend/common/observability/prometheus/sqlalchemy.py

# 日志系统
backend/app/admin/model/login_log.py
backend/app/admin/model/opera_log.py
backend/app/admin/schema/login_log.py
backend/app/admin/schema/opera_log.py
backend/app/admin/crud/crud_login_log.py
backend/app/admin/crud/crud_opera_log.py
backend/app/admin/service/login_log_service.py
backend/app/admin/service/opera_log_service.py
backend/common/queue.py

# 部署
deploy/backend/supervisor/fba_celery_beat.conf
deploy/backend/supervisor/fba_celery_flower.conf
deploy/backend/supervisor/fba_celery_worker.conf
deploy/backend/grafana/dashboards/fba_celery.json
```

---

## 已修改的文件

### 模型层

| 文件                                    | 修改内容                                |
|---------------------------------------|-------------------------------------|
| `backend/app/admin/model/__init__.py` | 仅保留 `User`、`UserPasswordHistory` 导出 |
| `backend/app/admin/model/user.py`     | 删除 `dept_id` 字段                     |

### Schema 层

| 文件                                 | 修改内容                                                                                                                                     |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `backend/app/admin/schema/user.py` | 删除 `dept_id`/`roles` 字段、`AddUserRoleParam`/`GetUserInfoWithRelationDetail`/`GetCurrentUserInfoWithRelationDetail`/`AddOAuth2UserParam` 类 |

### CRUD 层

| 文件                                    | 修改内容                                                                                                            |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `backend/app/admin/crud/crud_user.py` | 删除 Role/Dept/Menu/m2m 全部引用，移除 `get_join()` 方法、JoinConfig、m2m 操作；`add()`/`update()`/`delete()`/`get_select()` 简化 |

### Service 层

| 文件                                          | 修改内容                                                                              |
|---------------------------------------------|-----------------------------------------------------------------------------------|
| `backend/app/admin/service/user_service.py` | 删除 `get_roles()` 方法、dept/role 验证逻辑、`dept` 参数；`get_userinfo()` 改用 `user_dao.get()`/`get_by_username()`；`update_email()` 删除邮箱验证码（email 插件已移除），保留邮箱唯一性校验 |
| `backend/app/admin/service/auth_service.py` | 删除 `login_log_service`/`menu_dao` 引用、`get_codes()` 方法、`background_tasks` 参数       |

### Utils/安全层

| 文件                                 | 修改内容                                                                                                 |
|------------------------------------|------------------------------------------------------------------------------------------------------|
| `backend/app/admin/utils/cache.py` | 删除 `clear_by_role_id()`/`clear_by_menu_id()`/`clear_by_data_scope_id()`/`clear_by_data_rule_id()` 方法 |
| `backend/utils/trace_id.py`        | 删除 `OtelTraceIdPlugin` 类                                                                             |
| `backend/utils/dynamic_config.py`  | 保留上游懒加载 config 插件实现，删除邮箱插件相关 `load_email_config()`，仅保留用户安全与登录配置加载                       |

### API 层

| 文件                                           | 修改内容                                                                                            |
|----------------------------------------------|-------------------------------------------------------------------------------------------------|
| `backend/app/admin/api/v1/sys/user.py`       | 删除 `get_user_roles` 路由、`dept` 参数、`update_user_email` 的 captcha 参数；`delete_user` 改用 `DependsSuperUser`；响应类型改为 `GetUserInfoDetail` |
| `backend/app/admin/api/v1/sys/file.py`       | `RequestPermission + DependsRBAC` 改为 `DependsJwtAuth`                                           |
| `backend/app/admin/api/v1/sys/__init__.py`   | 仅保留 `user_router`、`file_router`、`plugin_router`                                                 |
| `backend/app/admin/api/v1/auth/auth.py`      | 删除 `get_codes` 路由、`background_tasks` 参数                                                         |
| `backend/app/admin/api/router.py`            | 删除 `monitor_router`、`log_router`                                                                |
| `backend/app/router.py`                      | 删除 `task_v1`                                                                                    |
| `backend/app/admin/api/v1/sys/plugin.py`     | `RequestPermission + DependsRBAC` 改为 `DependsSuperUser`                                         |
| `backend/plugin/config/api/v1/sys/config.py` | `RequestPermission + DependsRBAC` 改为 `DependsSuperUser`                                         |

### JWT/中间件层

| 文件                                           | 修改内容                                                                                                             |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| `backend/common/security/jwt.py`             | `GetUserInfoWithRelationDetail` → `GetUserInfoDetail`；`get_current_user()` 改用 `user_dao.get()`，删除 dept/role 状态检查；保留上游 `jwt_authentication_verify` 与 `TOKEN_REQUEST_UNDERLYING_SECURITY` |
| `backend/middleware/jwt_auth_middleware.py`  | `GetUserInfoWithRelationDetail` → `GetUserInfoDetail`                                                            |
| `backend/middleware/opera_log_middleware.py` | 移除 DB 队列/消费者/入库，改为纯控制台日志输出；异常码读取需包含 `__request_authentication_exception__` |
| `backend/middleware/access_middleware.py`    | 删除 Prometheus 导入和 2 处计数器调用                                                                                       |

### 核心层

| 文件                          | 修改内容                                                                                                                                       |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `backend/core/registrar.py` | 删除 socketio/prometheus/otel 导入、`register_socket_app()`、`register_metrics()`、OtelTraceIdPlugin、`create_task(OperaLogMiddleware.consumer())`；保留 lifespan `try/finally` 与上游 `dispose_database()` |
| `backend/core/conf.py`      | 删除 CELERY/GRAFANA/DATA_PERMISSION/OAUTH2/EMAIL/WS/CODE_GENERATOR/OPERA_LOG_*/RBAC_ROLE_MENU_*/CACHE_DICT_* 配置段；保留 `DATABASE_SOURCES`、`TOKEN_REQUEST_UNDERLYING_SECURITY`；`PLUGIN_REQUIRED` 仅保留 `config` |
| `backend/database/db.py`    | 删除 SQLAlchemy 连接池 Prometheus 指标监听                                                                                                        |
| `backend/alembic/env.py`    | 保持上游 `get_database_url()` 命名                                                                                                                |
| `backend/main.py`           | 保留上游插件准备流程 `_prepare_plugins()`，检查必需插件并安装缺失插件依赖                                                                                         |
| `backend/plugin/core.py`    | `get_required_plugins()` 删除 RBAC 模式相关 `casbin_rbac` 逻辑                                                                                      |
| `backend/plugin/hooks.py`   | 保留上游插件 setup/lifespan hooks，删除 OpenTelemetry hook                                                                                         |

### CLI

| 文件               | 修改内容                                                                             |
|------------------|----------------------------------------------------------------------------------|
| `backend/cli.py` | 删除 Celery/代码生成相关命令，保留插件安装卸载与依赖同步；`FbaCli.subcmd` 为 `Init \| Run \| Add \| Remove \| Deps \| Format \| Alembic` |

### Enum

| 文件                        | 修改内容                                                                                                                                            |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `backend/common/enums.py` | 删除 `MenuType`、`MethodType`、`BuildTreeType`、`RoleDataRuleOperatorType`、`RoleDataRuleExpressionType`、`LoginLogStatusType`、`OperaLogCipherType` 枚举；保留上游 `PluginLevelType.capability` |
| `backend/plugin/config/enums.py` | 仅保留 `ConfigType.user_security` 与 `ConfigType.login` |

### SQL 初始化数据

| 文件                                                    | 修改内容                                                                              |
|-------------------------------------------------------|-----------------------------------------------------------------------------------|
| `backend/sql/mysql/init_test_data.sql`                | 仅保留 sys_user INSERT（删除 dept/menu/role/role_menu/user_role/data_scope/data_rule 等） |
| `backend/sql/mysql/init_snowflake_test_data.sql`      | 同上                                                                                |
| `backend/sql/postgresql/init_test_data.sql`           | 同上                                                                                |
| `backend/sql/postgresql/init_snowflake_test_data.sql` | 同上                                                                                |
| `backend/plugin/config/sql/**/init*.sql`              | 删除 `sys_menu` 初始化与 EMAIL 配置，仅保留 `sys_config` 中用户安全/登录配置                         |
| `backend/plugin/config/sql/**/destroy*.sql`           | 删除 `sys_menu` 清理语句，仅保留 `sys_config` 清理                                            |

### 配置/部署

| 文件                                          | 修改内容                                                                                 |
|---------------------------------------------|--------------------------------------------------------------------------------------|
| `backend/.env.example`                      | 删除 Celery/RabbitMQ/OAuth2/Email 环境变量；保留 `DATABASE_SOURCES` |
| `pyproject.toml`                            | 项目名改为 `fba-slim`；删除 celery/socketio/opentelemetry/prometheus/psutil/flower/gevent/aio-pika/jinja2/psycopg/pymysql 等依赖；保留 `dulwich`（插件 Git 安装仍依赖） |
| `README.md` / `README.zh-CN.md`             | 使用 slim 专用说明，并指向完整版仓库 |
| `docker-compose.yml`                        | 删除 rabbitmq/celery/grafana 全套容器                                                      |
| `Dockerfile`                                | 简化为单一 server 镜像，删除 celery worker/beat/flower 阶段；保留插件依赖预安装步骤，用于打包随镜像发布的插件依赖 |
| `deploy/backend/docker-compose/.env.docker` | 删除 RabbitMQ/Celery/Grafana 端口映射                                                      |
| `deploy/backend/docker-compose/.env.server` | 删除 Celery/OAuth2/Email 环境变量                                                          |
| `deploy/backend/nginx.conf`                 | 删除 Flower 代理配置                                                                       |

---

## 插件依赖处理约定

- `Dockerfile` 必须保留 `# Preinstall plugin dependencies`，用于镜像构建时为随包插件安装依赖；当前随包插件仅有 `config`
- `backend/main.py` 必须保留上游 `_prepare_plugins()`，服务启动时会检查必需插件并安装缺失插件依赖
- 后续通过插件安装接口安装 zip/git 插件时，仍由 `backend/plugin/requirements.py` 安装该插件依赖

---

## 合并指南

从 fba 完整版同步代码到 fba-slim 后，需要关注以下冲突区域：

### 快速检测 rg 模式

合并后运行以下命令，快速找出需要处理的非 slim 引用：

```bash
# 全量残留扫描：唯一可接受命中是 OperaLogMiddleware 导入（控制台日志保留）
rg -n "celery|CELERY_|app\.task|python-socketio|socketio|prometheus|opentelemetry|psutil|flower|gevent|aio-pika|rabbitmq|GRAFANA_|OAUTH2_|EMAIL_CAPTCHA|CACHE_DICT|RBAC_ROLE_MENU|DATA_PERMISSION|RequestPermission|DependsRBAC|GetUserInfoWithRelation|GetCurrentUserInfoWithRelation|sys_menu|sys_role|sys_dept|data_scope|data_rule|login_log|opera_log|casbin_rbac|OtelTraceIdPlugin|init_plugin_otel|AddOAuth2UserParam" backend pyproject.toml Dockerfile docker-compose.yml deploy -g '!**/__pycache__/**'

# 精确 DB 日志 / RBAC / 数据权限残留扫描：应无命中
rg -n "opera_log_service|login_log_service|OPERA_LOG_|batch_dequeue|opera_log_queue|LoginLog|DataRule|DataScope|RequestPermission|DependsRBAC|GetUserInfoWithRelationDetail|CACHE_DICT_REDIS_PREFIX|EMAIL_CAPTCHA_REDIS_PREFIX" backend pyproject.toml Dockerfile docker-compose.yml deploy -g '!**/__pycache__/**'

# 已移除依赖残留扫描：应无命中
rg -n "celery|celery-aio|opentelemetry|prometheus-client|psutil|python-socketio|flower|gevent|aio-pika|psycopg|pymysql" pyproject.toml

# 内置插件校验：输出必须只有 config
find backend/plugin -mindepth 1 -maxdepth 1 -type d ! -name '__pycache__' -exec basename {} \; | sort
test "$(find backend/plugin -mindepth 1 -maxdepth 1 -type d ! -name '__pycache__' -exec basename {} \; | sort)" = config
```

> 注：slim 版仍保留 `backend/middleware/opera_log_middleware.py` 的 `OperaLogMiddleware`，用于控制台访问日志；检测 DB 日志残留时不要把该中间件类名视为问题。

### 高冲突文件

以下文件在完整版更新时最容易产生冲突：

1. **`backend/core/conf.py`** — 配置字段差异最大
2. **`backend/core/registrar.py`** — 中间件和组件注册差异
3. **`backend/cli.py`** — 删除 Celery/代码生成命令，保留插件 `Add`/`Remove`/`Deps`
4. **`backend/main.py`** — 上游插件准备流程必须保留
5. **`backend/common/security/jwt.py`** — `GetUserInfoDetail` vs `GetUserInfoWithRelationDetail`，`get_current_user()` 差异
6. **`backend/app/admin/crud/crud_user.py`** — 无 get_join/JoinConfig/m2m 操作
7. **`backend/app/admin/service/auth_service.py`** — 登录日志、menu_dao、background_tasks 差异
8. **`backend/middleware/opera_log_middleware.py`** — 完整版有 DB 队列，slim 版仅控制台
9. **`backend/middleware/jwt_auth_middleware.py`** — schema 类型差异
10. **`backend/plugin/config/sql/**`** — config 插件 SQL 不能再引用已删除的 `sys_menu`
11. **`pyproject.toml`** — 依赖列表差异
12. **`docker-compose.yml`** — 容器编排差异
13. **`Dockerfile`** — 构建阶段差异，需保留插件依赖预安装步骤但删除 Celery 多镜像阶段
14. **`deploy/backend/nginx.conf`** — Flower 代理容易残留

### 合并策略

1. **以上游新版本为基准**，只按本文档删除标准瘦身项，不要直接用旧 slim 文件覆盖上游正常演进
2. **需要手动合并**的文件：CRUD/Service/API 层（可能有新增功能需要保留，但需移除 RBAC/数据权限/可观测性引用）
3. **直接接受完整版**的文件：不涉及上述移除功能的纯业务逻辑改动
4. **合并后运行上述 `rg` 命令**清理残留引用
5. **插件依赖安装保持上游行为**：`backend/main.py` 启动时检测并安装缺失插件依赖，Dockerfile 构建时预装随包插件依赖
6. **运行 `fba format` 和导入检查**确认格式、锁文件、导出依赖和导入无误
7. **插件 CLI 必须保留**：插件核心系统完整保留，因此 `fba add` / `fba remove` / `fba deps` 与插件安装 API 一并保留；不要再删除插件安装卸载命令

### 验证清单

瘦身完成后至少运行：

```bash
fba format
uv run python -c "from backend.main import app; print(app.title); print(sorted(app.openapi()['paths']))"
```

> FastAPI 0.141+ 将 `include_router` 存为嵌套 `_IncludedRouter`，`len(app.routes)` 不再等于接口数量；请用 OpenAPI paths 核对。精简版应只有 auth/user/file/plugin/config，不应出现 role/menu/dept/log/monitor/task 或 AI 插件路由。
