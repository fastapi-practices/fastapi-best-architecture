# Email

电子邮件插件，提供邮件发送功能，支持验证码、通知等场景

- 支持 SMTP 邮件发送
- 支持验证码、通知等邮件场景
- 支持按基础配置控制邮箱服务、验证码有效期和 Redis 前缀

## 插件类型

- 应用级插件

## 配置说明

在 `backend/.env` 中添加以下内容：

```env
# [ Plugin ] email
EMAIL_USERNAME=''
EMAIL_PASSWORD=''
```

插件目录下 `plugin.toml` 的 `[settings]` 中包含以下内容：

```toml
[settings]
EMAIL_CAPTCHA_EXPIRE_SECONDS = 180
EMAIL_CAPTCHA_REDIS_PREFIX = 'fba:email:captcha'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_SSL = true
```

当前项目的 `backend/core/conf.py` 已包含以下字段：

```python
##################################################
# [ Plugin ] email
##################################################
# .env
EMAIL_USERNAME: str
EMAIL_PASSWORD: str

# 基础配置（in plugin.toml）
EMAIL_HOST: str
EMAIL_PORT: int
EMAIL_SSL: bool
EMAIL_CAPTCHA_REDIS_PREFIX: str
EMAIL_CAPTCHA_EXPIRE_SECONDS: int
```

## 配置项说明

- `EMAIL_CAPTCHA_EXPIRE_SECONDS`：控制邮箱验证码有效期
- `EMAIL_CAPTCHA_REDIS_PREFIX`：控制邮箱验证码 Redis 键前缀
- `EMAIL_HOST`：控制 SMTP 服务器地址
- `EMAIL_PORT`：控制 SMTP 端口
- `EMAIL_SSL`：控制是否启用 SSL

## 使用方式

1. 安装并启用插件后，配置正确的 SMTP 账号与密码
2. 根据实际邮箱服务商修改 `EMAIL_HOST`、`EMAIL_PORT`、`EMAIL_SSL`
3. 重启后端服务后，通过系统页面、Swagger 或业务代码使用邮件能力

## 卸载说明

- 卸载插件后，建议同步移除相关环境变量、插件基础配置和 `backend/core/conf.py` 中的插件配置
- 如业务代码仍在使用邮件发送能力，请同步清理对应集成

## 联系方式

- 作者：`wu-clan`
- 反馈方式：提交 Issue 或 PR
