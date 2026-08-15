# 油纸伞非遗文化数字平台 - 后端

基于 FastAPI + SQLAlchemy + SQLite 的后端服务。

## 功能模块

- 首页：轮播图、公告
- 文化历史：列表、详情
- 工艺展示：步骤列表、详情

## 运行步骤

1. 安装依赖

```
pip install -r requirements.txt
```

2. 启动服务

```
uvicorn app.main:app --reload