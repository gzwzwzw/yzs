from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from starlette.staticfiles import StaticFiles

from app.database import SessionLocal, engine
from app import models, schemas, crud
from app.schemas import InteractiveModelOut
from app.seed import init_db
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import (
    get_current_user, get_current_admin, create_access_token,
    get_password_hash, verify_password, oauth2_scheme
)

# 创建数据库表并初始化数据
models.Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="油纸伞非遗文化数字平台 API",
    description="提供油纸伞文化历史、工艺展示等数据接口",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

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

# ==================== 模型展示接口 ====================
@app.get("/api/interactive/models", response_model=List[InteractiveModelOut], tags=["互动体验"])
def get_interactive_models():
    """获取可用的3D模型列表"""
    models = [
        InteractiveModelOut(
            id=1,
            name="油纸伞三维模型",
            description="支持鼠标旋转、缩放，体验油纸伞结构之美",
            model_url="/static/models/oil_paper_umbrella.stl"
        )
    ]
    return models

# ==================== 认证接口 ====================
@app.post("/api/auth/register", response_model=schemas.UserOut, tags=["认证"])
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    new_user = crud.create_user(db, user.username, hashed)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token, tags=["认证"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserOut, tags=["认证"])
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# ==================== 管理员公告管理接口 ====================
@app.post("/api/admin/announcements", response_model=schemas.HomeAnnouncementOut, tags=["管理员"])
def admin_create_announcement(
    ann: schemas.AnnouncementCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    return crud.create_announcement(db, ann.title, ann.content)

@app.put("/api/admin/announcements/{ann_id}", response_model=schemas.HomeAnnouncementOut, tags=["管理员"])
def admin_update_announcement(
    ann_id: int,
    ann: schemas.AnnouncementUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    updates = {k: v for k, v in ann.dict(exclude_unset=True).items() if v is not None}
    updated = crud.update_announcement(db, ann_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return updated

@app.delete("/api/admin/announcements/{ann_id}", tags=["管理员"])
def admin_delete_announcement(
    ann_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    success = crud.delete_announcement(db, ann_id)
    if not success:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"message": "Announcement deleted"}