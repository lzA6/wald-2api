# wald-2api 🤖✨ - 你的 Wald.ai 超级充电站

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Stars](https://img.shields.io/github/stars/lzA6/wald-2api?style=social)
![Forks](https://img.shields.io/github/forks/lzA6/wald-2api?style=social)
![Issues](https://img.shields.io/github/issues/lzA6/wald-2api)

> **项目链接**: [https://github.com/lzA6/wald-2api](https://github.com/lzA6/wald-2api)

## 📖 项目简介

**wald-2api** 是一个高性能代理服务，将 `app.wald.ai` 的强大AI模型无缝转换为标准 OpenAI API 格式。让你的所有 OpenAI 兼容客户端和应用都能轻松使用 Wald.ai 的先进AI能力！

---

## 🎯 核心价值

在这个AI技术快速发展的时代，我们相信优秀的技术应该被更多人轻松使用。`wald-2api` 的使命是：

> **打破技术壁垒，让强大的AI能力像水电一样普及，流淌到每一个需要它的角落。**

无论你是开发者、研究者还是AI爱好者，这个项目都将为你打开一扇通往先进AI模型的大门。

---

## ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🚀 **极致性能** | 基于 FastAPI 和 Uvicorn，天生异步，响应迅捷 | ✅ 已实现 |
| 🌍 **OpenAI 兼容** | 完美模拟 `/v1/chat/completions` 和 `/v1/models` 接口 | ✅ 已实现 |
| 🌊 **流式传输** | 完整的流式响应支持，打字机效果流畅 | ✅ 已实现 |
| 📦 **一键部署** | Docker 和 docker-compose 支持，快速启动 | ✅ 已实现 |
| 🔐 **安全可靠** | API_MASTER_KEY 访问控制，防止滥用 | ✅ 已实现 |
| 🔧 **高度可配置** | 通过环境变量轻松配置所有参数 | ✅ 已实现 |
| 🧠 **智能过滤** | 自动清理 Wald.ai 内部思考过程，输出纯净答案 | ✅ 已实现 |

---

## 🏗️ 系统架构

```mermaid
graph TB
    A[客户端应用] --> B[wald-2api 代理服务]
    B --> C[Wald.ai 官方API]

    subgraph "wald-2api 内部架构"
        B1[FastAPI Web框架] --> B2[路由层]
        B2 --> B3[Wald Provider]
        B3 --> B4[SSE 流式处理]
        B3 --> B5[数据清洗]
    end

    subgraph "客户端兼容性"
        A1[OpenAI SDK] --> B
        A2[第三方客户端] --> B
        A3[自定义应用] --> B
    end
```

---

## 📁 项目结构

```
wald-2api/
├── .env                    # 环境配置文件
├── .env.example            # 环境配置模板
├── Dockerfile              # 容器构建配置
├── docker-compose.yml      # 服务编排配置
├── main.py                 # FastAPI 应用入口
├── nginx.conf              # Nginx 反向代理配置
├── requirements.txt        # Python 依赖清单
└── app/
    ├── core/
    │   ├── __init__.py
    │   └── config.py       # 配置管理核心
    ├── providers/
    │   ├── __init__.py
    │   ├── base_provider.py # Provider 抽象基类
    │   └── wald_provider.py # Wald.ai 适配器
    └── utils/
        └── sse_utils.py    # 流式事件工具
```

---

## 🔄 工作原理

### 数据流转流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant W as wald-2api
    participant A as Wald.ai

    C->>W: 发送 OpenAI 格式请求
    Note over W: 接收并验证请求

    W->>W: 转换请求格式
    Note over W: _prepare_payload()<br/>生成 UUID<br/>构建消息链

    W->>A: 发送 Wald.ai 原生请求
    Note over W: 携带 WOS_SESSION_COOKIE

    A->>W: 返回流式响应
    Note over A: 原始数据流<br/>包含内部工作流程

    W->>W: 数据清洗和转换
    Note over W: stream_generator()<br/>过滤内部思考<br/>格式标准化

    W->>C: 返回 OpenAI 格式响应
    Note over W: 纯净的流式数据
```

### 核心转换过程

1. **请求适配**：将 OpenAI 格式的 `messages` 数组转换为 Wald.ai 所需的复杂 JSON 结构
2. **身份验证**：使用 `WOS_SESSION_COOKIE` 维持会话状态
3. **流式处理**：实时处理 Wald.ai 的 SSE 响应，逐行解析和清洗
4. **数据净化**：使用正则表达式过滤 `<<<Workflow...` 等内部信息
5. **格式标准化**：重新包装为 OpenAI 兼容的数据格式

---

## 🛠️ 技术栈深度解析

| 组件 | 作用 | 技术优势 | 实施难度 |
|------|------|----------|----------|
| **FastAPI** | Web 框架 | 高性能、自动文档生成、类型安全 | ⭐⭐☆☆☆ |
| **Uvicorn** | ASGI 服务器 | 基于 uvloop 的极致性能 | ⭐☆☆☆☆ |
| **Docker** | 容器化 | 环境一致性、快速部署 | ⭐⭐⭐☆☆ |
| **Nginx** | 反向代理 | 负载均衡、静态文件服务 | ⭐⭐☆☆☆ |
| **httpx** | HTTP 客户端 | 全功能异步、HTTP/2 支持 | ⭐⭐☆☆☆ |
| **Pydantic** | 数据验证 | 类型提示、自动数据校验 | ⭐★☆☆☆ |

---

## 🚀 快速开始

### 环境准备

1. **安装 Git**: [下载地址](https://git-scm.com/downloads)
2. **安装 Docker**: [下载地址](https://www.docker.com/products/docker-desktop/)

### 步骤 1: 获取身份凭证

获取 `WOS_SESSION_COOKIE` 是使用服务的关键：

1. 打开浏览器并访问 [Wald.ai](https://app.wald.ai/)
2. 登录你的账户
3. 按 `F12` 打开开发者工具
4. 切换到 **Network** 标签页
5. 在 Wald.ai 中发送一条消息
6. 找到名为 `chat` 的请求
7. 在请求头中复制完整的 `wos-session` Cookie 值

**注意**: Cookie 值以 `Fe26.` 开头，非常长，请确保完整复制！

### 步骤 2: 配置服务

```bash
# 克隆项目
git clone https://github.com/lzA6/wald-2api.git
cd wald-2api

# 复制配置文件
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用你喜欢的编辑器
```

配置文件内容示例：
```env
API_MASTER_KEY=sk-your-super-secret-key-here
NGINX_PORT=8088
WOS_SESSION_COOKIE="你的完整Cookie字符串"
```

### 步骤 3: 启动服务

```bash
# 使用 docker-compose 一键启动
docker-compose up -d
```

服务将在 `http://localhost:8088` 启动。

### 步骤 4: 验证服务

使用 curl 测试服务：

```bash
curl http://localhost:8088/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-super-secret-key-here" \
  -d '{
    "model": "gpt-5",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "stream": true
  }'
```

---

## 💡 使用场景

### 适用场景

| 场景 | 描述 | 收益 |
|------|------|------|
| **个人项目** | 在个人应用中使用 Wald.ai 模型 | 快速集成，无需复杂适配 |
| **团队工具** | 团队内部基于 OpenAI API 的工具链 | 平滑引入新模型供应商 |
| **研究实验** | AI 模型对比和研究 | 统一接口，简化实验设计 |
| **第三方集成** | 支持 OpenAI API 的客户端和应用 | 扩展应用能力范围 |

### 客户端配置示例

**OpenAI 官方 SDK**:
```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8088/v1",
    api_key="sk-your-super-secret-key-here"
)

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**第三方客户端**:
- 将 API Base URL 设置为: `http://localhost:8088/v1`
- API Key 设置为: `sk-your-super-secret-key-here`

---

## 📊 项目现状

### ✅ 已实现功能

- [x] 核心的 OpenAI API 兼容层
- [x] 流式和非流式响应支持
- [x] 多模型别名映射
- [x] 完整的 Docker 部署方案
- [x] API 密钥认证系统
- [x] Wald.ai 内部信息过滤

### ⚠️ 当前限制

1. **Cookie 管理**: 需要手动更新过期的 `WOS_SESSION_COOKIE`
2. **静态模型列表**: 模型映射硬编码，不支持动态发现
3. **功能范围**: 仅支持聊天补全，缺少文件上传等高级功能

---

## 🗺️ 发展路线图

### V1.5 - 自动化改进
- **自动 Cookie 刷新**: 实现会话自动续期
- **基础监控**: 添加健康检查和基础指标
- **文档完善**: 完整的 API 文档和使用指南

### V2.0 - 功能扩展
- **动态模型发现**: 自动同步 Wald.ai 可用模型
- **多租户支持**: 支持多个 API Key 和用量统计
- **高级特性**: 适配文件上传、函数调用等功能

### V2.5 - 生态集成
- **Web 管理界面**: 图形化配置和管理
- **插件系统**: 支持扩展其他 AI 服务提供商
- **性能优化**: 缓存、连接池等性能提升

### V3.0 - 平台化
- **用户系统**: 完整的用户认证和权限管理
- **计费系统**: 使用量统计和计费支持
- **高可用**: 集群部署和负载均衡

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是代码、文档、问题反馈还是功能建议。

### 贡献流程

1. Fork 本仓库
2. 创建功能分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/lzA6/wald-2api.git
cd wald-2api

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件设置你的配置

# 启动开发服务器
uvicorn main:app --reload --port 8088
```

---

## 📄 开源协议

本项目采用 **Apache License 2.0** 开源协议。

**你可以**:
- ✅ 自由使用（商业或非商业）
- ✅ 自由分发和复制
- ✅ 自由修改源代码

**你需要**:
- 📝 保留原始版权和许可声明
- 📝 声明代码修改内容

这是一个对商业友好的开源协议，让你可以放心使用和集成。

---

## 🆘 常见问题

### Q: Cookie 过期了怎么办？
A: 目前需要手动重新获取并更新 `.env` 文件中的 `WOS_SESSION_COOKIE` 值，然后重启服务。

### Q: 支持哪些模型？
A: 目前支持通过 `MODEL_MAPPING` 配置的模型别名，如 "gpt-5"、"claude-3" 等。

### Q: 如何查看服务日志？
A: 使用命令 `docker-compose logs -f` 查看实时日志。

### Q: 性能如何？
A: 在标准硬件上，响应延迟主要取决于 Wald.ai 服务的响应时间，代理本身引入的延迟可以忽略不计。

---

## 📞 支持与反馈

如果你遇到问题或有建议：

1. 查看 [Issues](https://github.com/lzA6/wald-2api/issues) 页面
2. 提交新的 Issue 描述问题
3. 或通过讨论区交流想法

---

**感谢你使用 wald-2api！愿这个工具能为你的 AI 之旅增添力量。🌟**

*一起让 AI 技术更加普及和易用！*
