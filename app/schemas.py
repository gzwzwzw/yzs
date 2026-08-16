from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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