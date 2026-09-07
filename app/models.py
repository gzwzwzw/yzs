from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta, timezone

def get_beijing_time():
    """获取当前北京时间（无时区信息）"""
    beijing_tz = timezone(timedelta(hours=8))
    return datetime.now(beijing_tz).replace(tzinfo=None)

class HomeBanner(Base):
    """首页轮播图"""
    __tablename__ = "home_banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=False)
    link_url = Column(String(255), default="")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class HomeAnnouncement(Base):
    """首页公告/资讯"""
    __tablename__ = "home_announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    publish_time = Column(DateTime, default=get_beijing_time)

    is_active = Column(Boolean, default=True)


class CulturalHistory(Base):
    """文化历史条目"""
    __tablename__ = "cultural_histories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    period = Column(String(50), nullable=False)          # 时期，如“春秋战国”
    summary = Column(Text, nullable=False)               # 摘要
    content = Column(Text, nullable=False)               # 详细内容
    image_url = Column(String(255), default="")
    video_url = Column(String(255), default="")
    region = Column(String(50), default="")              # 地域流派
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class CraftStep(Base):
    """工艺步骤"""
    __tablename__ = "craft_steps"

    id = Column(Integer, primary_key=True, index=True)
    step_number = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(255), default="")
    video_url = Column(String(255), default="")
    material = Column(String(255), default="")           # 所需材料
    tool = Column(String(255), default="")               # 使用工具
    duration = Column(String(50), default="")            # 耗时
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # "user" 或 "admin"
    created_at = Column(DateTime, default=get_beijing_time)
    avatar_url = Column(String(255), default="", nullable=True)  # 新增头像字段

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# 在现有模型后添加
class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)
    content_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=get_beijing_time)
    __table_args__ = (UniqueConstraint('user_id', 'content_type', 'content_id', name='_user_content_uc'),)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)
    content_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=get_beijing_time)

    user = relationship("User")