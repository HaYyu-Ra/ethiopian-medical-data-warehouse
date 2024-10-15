from sqlalchemy import Column, Integer, String, Date
from database import Base

class CleanedData(Base):
    __tablename__ = "cleaned_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    date_recorded = Column(Date)

    # Add more fields as per your requirements
