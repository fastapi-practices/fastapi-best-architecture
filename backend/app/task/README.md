## 任务介绍

当前任务使用 Celery
实现，实施方案请查看 [#225](https://github.com/fastapi-practices/fastapi-best-architecture/discussions/225)

## 定时任务

在 `backend/app/task/tasks/beat.py` 文件内编写相关定时任务

### 简单任务

在 `backend/app/task/tasks/tasks.py` 文件内编写相关任务代码

### 层级任务

如果你想对任务进行目录层级划分，使任务结构更加清晰，你可以新建任意目录，但必须注意的是

1. 在 `backend/app/task/tasks` 目录下新建 python 包目录
2. 在新建目录下，务必添加 `tasks.py` 文件，并在此文件中编写相关任务代码

## 消息代理

你可以通过 `CELERY_BROKER` 控制消息代理选择，它支持 redis 和 rabbitmq

对于本地调试，建议使用 redis

对于线上环境，强制使用 rabbitmq

## Flower 只读监控

`fba celery flower` 默认启用只读模式，允许查看 worker 和任务，禁止撤销任务、调整进程池、关闭 worker 等管理操作。Supervisor 部署也显式启用只读模式。

需要管理操作时，使用 `fba celery flower --no-read-only`。部署方式可将 `fba_celery_flower.conf` 中的 `--read-only=True` 改为 `--read-only=False`。

Flower 2.2 对跨站写请求进行校验，反向代理应保留正确的 Host；同源 Basic Auth 页面无需额外的 cookie XSRF token。
