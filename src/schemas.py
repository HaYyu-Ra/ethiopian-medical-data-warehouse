from pydantic import BaseModel

class CleanedDataCreate(BaseModel):
    field1: str
    field2: str
    field3: int
    field4: bool

class CleanedDataRead(BaseModel):
    id: int
    field1: str
    field2: str
    field3: int
    field4: bool

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility
