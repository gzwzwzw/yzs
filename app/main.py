from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal, engine
from app import models, schemas, crud
from app.seed import init_db

# 创建数据库表并初始化数据
models.Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="油纸伞非遗文化数字平台 API",
    description="提供油纸伞文化历史、工艺展示等数据接口",
    version="1.0.0"
)

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 依赖：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 首页接口 ====================
@app.get("/api/home/banners", response_model=List[schemas.HomeBannerOut], tags=["首页"])
def get_home_banners(db: Session = Depends(get_db)):
    """获取首页轮播图"""
    banners = crud.get_active_banners(db)
    return banners


@app.get("/api/home/announcements", response_model=List[schemas.HomeAnnouncementOut], tags=["首页"])
def get_home_announcements(db: Session = Depends(get_db)):
    """获取首页公告"""
    announcements = crud.get_active_announcements(db)
    return announcements


# ==================== 文化历史接口 ====================
@app.get("/api/history", response_model=List[schemas.CulturalHistoryListOut], tags=["文化历史"])
def get_cultural_history_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取文化历史列表（分页）"""
    items = crud.get_cultural_history_list(db, skip=skip, limit=limit)
    return items


@app.get("/api/history/{history_id}", response_model=schemas.CulturalHistoryDetailOut, tags=["文化历史"])
def get_cultural_history_detail(history_id: int, db: Session = Depends(get_db)):
    """获取文化历史详情"""
    item = crud.get_cultural_history_detail(db, history_id)
    if not item:
        raise HTTPException(status_code=404, detail="未找到该文化历史条目")
    return item


# ==================== 工艺展示接口 ====================
@app.get("/api/craft", response_model=List[schemas.CraftStepOut], tags=["工艺展示"])
def get_craft_steps(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取工艺步骤列表（分页）"""
    items = crud.get_craft_steps(db, skip=skip, limit=limit)
    return items


@app.get("/api/craft/{step_id}", response_model=schemas.CraftStepOut, tags=["工艺展示"])
def get_craft_step_detail(step_id: int, db: Session = Depends(get_db)):
    """获取工艺步骤详情"""
    item = crud.get_craft_step_detail(db, step_id)
    if not item:
        raise HTTPException(status_code=404, detail="未找到该工艺步骤")
    return item


@app.get("/", tags=["系统"])
def root():
    return {"message": "油纸伞非遗文化数字平台 API", "docs": "/docs"}