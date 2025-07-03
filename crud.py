# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_gift(db: Session, gift_id: int):
    return db.query(models.Gift).filter(models.Gift.id == gift_id).first()

def get_gifts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gift).offset(skip).limit(limit).all()

def create_gift(db: Session, gift: schemas.GiftCreate):
    db_gift = models.Gift(**gift.dict())
    db.add(db_gift)
    db.commit()
    db.refresh(db_gift)
    return db_gift
