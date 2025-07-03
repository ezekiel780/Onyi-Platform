from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, schemas, crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Gift API",
    description="A simple gift management API",
    version="1.0.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Gift API! 🎁"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/gifts/{gift_id}", response_model=schemas.Gift)
def get_gift(gift_id: int, db: Session = Depends(get_db)):
    gift = db.query(models.Gift).filter(models.Gift.id == gift_id).first()
    if gift is None:
        raise HTTPException(status_code=404, detail="Gift not found")
    return gift

@app.get("/gifts/", response_model=list[schemas.Gift])
def list_gifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gifts = db.query(models.Gift).offset(skip).limit(limit).all()
    return gifts

@app.post("/gifts/", response_model=schemas.Gift)
def create_gift(gift_data: schemas.GiftCreate, db: Session = Depends(get_db)):
    gift = models.Gift(**gift_data.dict())
    db.add(gift)
    db.commit()
    db.refresh(gift)
    return gift
