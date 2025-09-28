from sqlalchemy.orm import Session
from app import models,schemas


def get_all_mis(db: Session):
    return db.query(models.MIS_Table).all()

def create_mis(db: Session, mis: schemas.MISCreate):
    db_mis = models.MIS_Table(**mis.dict())
    db.add(db_mis)
    db.commit()
    db.refresh(db_mis)
    return db_mis