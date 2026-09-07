# Code Generator

代码生成器插件，生成通用业务代码

- 支持维护代码生成业务配置与模型列信息
- 支持手动模式和自动导表模式生成通用业务代码
- 支持预览、写入磁盘和下载生成结果

## 插件类型

- 应用级插件

## 配置说明

插件目录下 `plugin.toml` 的 `[settings]` 中包含以下内容：

```toml
[settings]
CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME = 'fba_generator'
```

当前项目的 `backend/core/conf.py` 已包含以下字段：

```python
##################################################
# [ Plugin ] code_generator
##################################################
CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME: str
```

## 配置项说明

- `CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME`：控制代码生成结果下载压缩包的文件名

## 使用方式

1. 安装并启用插件后，重启后端服务
2. 维护业务配置和模型列信息
3. 执行预览、生成和下载流程
4. 生成代码会直接写入磁盘，仅必须在开发环境使用

## 卸载说明

- 卸载插件后，建议同步移除相关插件基础配置和 `backend/core/conf.py` 中的插件配置
- 如项目中已接入代码生成相关页面或自动化流程，请同步清理对应集成

## 联系方式

- 作者：`wu-clan`
- 反馈方式：提交 Issue 或 PR
