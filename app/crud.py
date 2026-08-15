from sqlalchemy.orm import Session
from app import models


def get_active_banners(db: Session, limit: int = 5):
    return (db.query(models.HomeBanner)
            .filter(models.HomeBanner.is_active == True)
            .order_by(models.HomeBanner.sort_order)
            .limit(limit)
            .all())


def get_active_announcements(db: Session, limit: int = 10):
    return (db.query(models.HomeAnnouncement)
            .filter(models.HomeAnnouncement.is_active == True)
            .order_by(models.HomeAnnouncement.publish_time.desc())
            .limit(limit)
            .all())


def get_cultural_history_list(db: Session, skip: int = 0, limit: int = 20):
    return (db.query(models.CulturalHistory)
            .filter(models.CulturalHistory.is_active == True)
            .order_by(models.CulturalHistory.sort_order)
            .offset(skip)
            .limit(limit)
            .all())


def get_cultural_history_detail(db: Session, history_id: int):
    return (db.query(models.CulturalHistory)
            .filter(models.CulturalHistory.id == history_id,
                    models.CulturalHistory.is_active == True)
            .first())


def get_craft_steps(db: Session, skip: int = 0, limit: int = 50):
    return (db.query(models.CraftStep)
            .filter(models.CraftStep.is_active == True)
            .order_by(models.CraftStep.step_number)
            .offset(skip)
            .limit(limit)
            .all())


def get_craft_step_detail(db: Session, step_id: int):
    return (db.query(models.CraftStep)
            .filter(models.CraftStep.id == step_id,
                    models.CraftStep.is_active == True)
            .first())