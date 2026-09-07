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

# 用户相关
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password_hash: str, role: str = "user"):
    user = models.User(username=username, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 公告管理
def create_announcement(db: Session, title: str, content: str):
    ann = models.HomeAnnouncement(title=title, content=content)
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann

def update_announcement(db: Session, ann_id: int, updates: dict):
    ann = db.query(models.HomeAnnouncement).filter(models.HomeAnnouncement.id == ann_id).first()
    if not ann:
        return None
    for key, value in updates.items():
        setattr(ann, key, value)
    db.commit()
    db.refresh(ann)
    return ann

def delete_announcement(db: Session, ann_id: int):
    ann = db.query(models.HomeAnnouncement).filter(models.HomeAnnouncement.id == ann_id).first()
    if not ann:
        return False
    db.delete(ann)
    db.commit()
    return True

# 点赞相关
def get_like(db: Session, user_id: int, content_type: str, content_id: int):
    return db.query(models.Like).filter(
        models.Like.user_id == user_id,
        models.Like.content_type == content_type,
        models.Like.content_id == content_id
    ).first()

def add_like(db: Session, user_id: int, content_type: str, content_id: int):
    like = models.Like(user_id=user_id, content_type=content_type, content_id=content_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def remove_like(db: Session, like: models.Like):
    db.delete(like)
    db.commit()

def get_like_count(db: Session, content_type: str, content_id: int):
    return db.query(models.Like).filter(
        models.Like.content_type == content_type,
        models.Like.content_id == content_id
    ).count()

# 评论相关
def get_comments(db: Session, content_type: str, content_id: int):
    return db.query(models.Comment).filter(
        models.Comment.content_type == content_type,
        models.Comment.content_id == content_id
    ).order_by(models.Comment.created_at.desc()).all()

def add_comment(db: Session, user_id: int, content_type: str, content_id: int, text: str):
    comment = models.Comment(user_id=user_id, content_type=content_type, content_id=content_id, text=text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
