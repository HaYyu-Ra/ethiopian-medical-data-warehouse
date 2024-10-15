from sqlalchemy.orm import Session
from models import CleanedData
from schemas import CleanedDataCreate

def create_cleaned_data(db: Session, cleaned_data: CleanedDataCreate):
    db_cleaned_data = CleanedData(**cleaned_data.dict())
    db.add(db_cleaned_data)
    db.commit()
    db.refresh(db_cleaned_data)
    return db_cleaned_data

def get_cleaned_data(db: Session):
    return db.query(CleanedData).all()

# Additional CRUD operations (Update, Delete) can be added similarly
