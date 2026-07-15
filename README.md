# WeChat RPA recovered source

本仓库保存从 `yoko_rpa_mcp.exe`（PyInstaller / CPython 3.12）恢复的 Python
源码，以及在恢复源码基础上整理的本地开发版本。

## 直接使用

不需要自行编译恢复源码。Windows 用户可以下载
[`yoko_rpa_mcp_noverify.zip`](https://github.com/Usernames686/wechat/releases/download/v1.8.4-local-dev/yoko_rpa_mcp_noverify.zip)，
完整解压后双击 `start_noverify.cmd`。便携版包含独立本地认证组件，不要求系统安装
Python，也不依赖云端许可服务；启动成功后会自动打开 `http://127.0.0.1:9922/`。

发布包 SHA-256：

```text
C7FDF802E4502DCB00FC0703E69D39684CBB89F0D4B4FB648E328B75392BAA1E
```

详细配置和 MCP 接入方式见 [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md)。

## 目录

| 目录 | 内容 |
| --- | --- |
| `recovered_source/` | 从应用字节码恢复的源码，尽量保持恢复时的结构和逻辑。 |
| `unlocked_source/` | 本地开发版本，许可状态、HTTP 许可中间件和 MCP 许可解析已替换为本地响应。 |

本地开发版本的具体修改见
[`unlocked_source/UNLOCKED_CHANGES.md`](unlocked_source/UNLOCKED_CHANGES.md)。

## 本地开发版本改动

- `WeRobotCore/utils/license_manager.py`：使用本地开发许可数据，不访问远程许可服务。
- `api_server.py`：HTTP 许可中间件直接放行，并提供本地开发账号响应。
- `mcp_gateway.py`：MCP 许可归属解析使用本机生成的数据。

上述三个修改文件已经通过 CPython `py_compile` 检查；`LicenseManager` 的本地状态、
许可信息和机器码响应也已单独验证。

## 恢复源码状态

这些文件是反编译恢复结果，不等同于原始工程源码。控制流恢复过程中仍有部分模块包含：

- 函数外 `return`；
- 被错误还原的函数调用或下标表达式；
- 丢失的异常处理和分支结构；
- 编码受损的中文字符串。

因此本仓库适合代码检查、逻辑定位和继续手工恢复，目前不保证能够直接重新打包为 EXE。
恢复结果中 84/132 个模块可完整编译，其余模块需要结合 CPython 3.12 字节码或反汇编继续修复。

## 公开仓库脱敏

提交前已将恢复结果里的邮件授权口令、客户标识、客户服务地址和 API 凭据替换为占位值。
运行时产生的 `.env`、本地许可文件、MCP 配对令牌、日志、数据库和 Python 缓存也由
`.gitignore` 排除。

需要外部服务的功能通过环境变量或应用控制台填写使用者自己的凭据；可复制
[`.env.example`](.env.example) 作为源码配置模板。

## 版本信息

- 应用版本：`1.8.4`
- 打包方式：PyInstaller
- Python 字节码版本：CPython 3.12
- 恢复日期：2026-07-15
