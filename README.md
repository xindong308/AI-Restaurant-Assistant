# FastAPI AI Agent AI赋能幸福餐厅项目

基于 FastAPI 和 LangChain 构建的智能 AI 助手系统，集成了通义千问大模型和 Elasticsearch 向量检索，为用户提供智能问答和数据分析服务。

## 功能特性

- 🤖 **双 Agent 系统**
  - **用户 Agent**: 面向终端用户的智能客服助手
  - **管理员 Agent**: 面向管理员的数据分析和报表生成助手

- 🧠 **AI 能力**
  - 集成通义千问 (Qwen) 大语言模型
  - Elasticsearch 向量相似度检索
  - RAG (检索增强生成) 技术
  - 多轮对话上下文管理

- 🔧 **工具集**
  - 订单查询与分析
  - 销售数据统计
  - 自动生成销售报表
  - 实时时间查询
  - 文档摘要生成

- 💾 **数据存储**
  - Redis 会话管理
  - MySQL 数据库支持
  - Elasticsearch 向量数据库

## 项目结构

```
FastAPI/
├── Agent/                      # Agent 核心模块
│   ├── admin_agent.py         # 管理员 Agent
│   ├── user_agent.py          # 用户 Agent
│   └── tools/                 # Agent 工具集
│       ├── admin_agent_tools.py
│       ├── user_agent_tools.py
│       └── middleware.py
├── config/                     # 配置文件
│   ├── rag.yml                # RAG 模型配置
│   ├── redis.yml              # Redis 配置
│   └── *.txt                  # Prompt 模板
├── model/                      # 数据模型
│   └── input.py               # 输入数据模型
├── utils/                      # 工具函数
│   ├── config_handler.py      # 配置处理
│   ├── redis_client.py        # Redis 客户端
│   ├── mysql_hander.py        # MySQL 处理
│   ├── logger_handler.py      # 日志处理
│   └── prompt_util.py         # Prompt 工具
├── ai_answer.py               # AI 回答核心模块
├── main.py                    # FastAPI 主应用
└── requirements.txt           # Python 依赖
```

## 快速开始

### 环境要求

- Python 3.10+
- Redis 服务器
- MySQL 数据库
- Elasticsearch 8.0+
- DashScope API 密钥

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. **配置 DashScope API**
   - 在 `config/rag.yml` 中配置模型名称
   - 确保已设置 `DASHSCOPE_API_KEY` 环境变量

2. **配置 Redis**
   - 编辑 `config/redis.yml` 设置 Redis 连接参数

3. **配置 Elasticsearch**
   - 在 `ai_answer.py` 中配置 ES 地址和索引名称

### 运行服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 `http://localhost:8000/docs` 查看 API 文档。

## API 接口

### 基础接口

- `GET /` - 欢迎接口
- `GET /hello/{name}` - 问候接口

### AI 对话接口

#### 用户 AI 对话
```bash
POST /user/ai
Content-Type: application/json

{
  "id": "user_id",
  "query": "你的问题"
}
```

#### 管理员 AI 对话
```bash
POST /admin/ai
Content-Type: application/json

{
  "id": "employee_id",
  "query": "你的问题"
}
```

## 主要功能示例

### 用户 Agent 功能
- 查询个人订单信息
- 订单状态查询
- 智能客服问答

### 管理员 Agent 功能
- 销售数据统计
- 利润分析
- 订单信息查询
- 自动生成销售报表
- 时间查询

## 技术栈

- **Web 框架**: FastAPI
- **AI 框架**: LangChain
- **大模型**: 通义千问 (Qwen)
- **向量检索**: Elasticsearch
- **缓存**: Redis
- **数据库**: MySQL
- **异步**: asyncio

## 配置文件说明

### config/rag.yml
```yaml
chat_model_name: qwen-plus
embedding_model_name: text-embedding-v4
```

### config/redis.yml
```yaml
REDIS_HOST: localhost
REDIS_PORT: 6379
REDIS_DB: 1
```

## 开发说明

### 添加新工具

在 `Agent/tools/` 目录下创建新的工具函数，并在对应的 Agent 中注册。

### 自定义 Prompt

在 `config/` 目录下编辑 `admin_prompt.txt` 或 `user_prompt.txt` 文件。

## 注意事项

- 本项目需要有效的 DashScope API 密钥
- Elasticsearch 需要预先创建好索引
- Redis 和 MySQL 服务需要运行
- 生产环境请修改默认配置并设置适当的安全措施

## License

MIT License

## 联系方式

如有问题，请提交 3084552610@qq.com 或联系开发者。
