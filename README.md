# ChatGPT-Proxy
Forward requests and inject CloudFlare cookies

# > Unmaintained 

## Installation

### One-click scripts 

- With Docker: `curl https://raw.githubusercontent.com/acheong08/ChatGPT-Proxy/main/scripts/run-with-docker.sh | sh`


### Simple steps

1. Clone the repository
2. Check if Pipenv is installed. If not, run `pip install pipenv -U`.
3. Then, run `pipenv update -d` in this directory, to automatically install the requirements of the proxy.
4. Run `pipenv run proxy` in the base directory, and enjoy it! Uvicorn will provide a high-performance HTTP server for the API service.


### Options

These options can be configured by setting environment variables using `-e KEY="VALUE"` in the `docker run` command.

| Env | Default | Example | Description |
| - | - | - | - |
| `GPT_PROXY` | - | `socks5://127.0.0.1:1080` | The proxy of your server. |
| `GPT_HOST` | `0.0.0.0` | `127.0.0.1` | The hostname of your server. |
| `GPT_PORT` | `5000` | `8080` | The port of your server. |


# ChatGPT 代理
转发请求并注入 CloudFlare cookie

# > 无人维护

＃＃ 安装

### 一键脚本

- 使用 Docker：`curl https://raw.githubusercontent.com/acheong08/ChatGPT-Proxy/main/scripts/run-with-docker.sh | sh`


### 简单步骤

1.克隆存储库
2.检查是否安装了Pipenv。 如果没有，请运行“pip install pipenv -U”。
3. 然后，在此目录中运行`pipenv update -d`，自动安装代理的要求。
4. 在根目录下运行`pipenv run proxy`，尽情享受吧！ Uvicorn 将为 API 服务提供高性能的 HTTP 服务器。


＃＃＃ 选项

这些选项可以通过在 `docker run` 命令中使用 `-e KEY="VALUE"` 设置环境变量来配置。

| 环境 | 默认 | 范例 | 说明 |
| - | - | - | - |
| `GPT_PROXY` | - | `socks5://127.0.0.1:1080` | 您的服务器的代理。 |
| `GPT_HOST` | `0.0.0.0` | `127.0.0.1` | 服务器的主机名。 |
| `GPT_PORT` | `5000` | `8080` | 服务器的端口。 |

proxy2.py修改说明
对 chat.openai.com 的所有请求使用 HTTPS 而不是 HTTP 来加密客户端和服务器之间交换的数据。

使用环境变量来存储敏感信息，例如 API 密钥，而不是将它们硬编码在代码中。

验证客户端发送的授权标头以确保它包含有效的令牌或 API 密钥。

实施速率限制以防止服务器滥用或过载。

实施错误处理以优雅地处理代码执行过程中可能发生的异常和错误。
