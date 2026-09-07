from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ===== 用户认证 =====
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

# ===== 公告管理 =====
class AnnouncementCreate(BaseModel):
    title: str
    content: str

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class HomeBannerOut(BaseModel):
    id: int
    title: str
    image_url: str
    link_url: str
    sort_order: int

    class Config:
        from_attributes = True


class HomeAnnouncementOut(BaseModel):
    id: int
    title: str
    content: str
    publish_time: datetime

    class Config:
        from_attributes = True


class CulturalHistoryListOut(BaseModel):
    id: int
    title: str
    period: str
    summary: str
    image_url: str
    region: str

    class Config:
        from_attributes = True


class CulturalHistoryDetailOut(BaseModel):
    id: int
    title: str
    period: str
    summary: str
    content: str
    image_url: str
    video_url: str
    region: str

    class Config:
        from_attributes = True


class CraftStepOut(BaseModel):
    id: int
    step_number: int
    title: str
    description: str
    image_url: str
    video_url: str
    material: str
    tool: str
    duration: str

    class Config:
        from_attributes = True

class InteractiveModelOut(BaseModel):
    id: int
    name: str
    description: str
    model_url: str

    class Config:
        from_attributes = True