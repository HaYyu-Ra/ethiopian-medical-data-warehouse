from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import create_cleaned_data, get_cleaned_data
from schemas import CleanedDataRead, CleanedDataCreate

app = FastAPI()

@app.post("/cleaned_data/", response_model=CleanedDataRead)
async def create_cleaned_data_route(cleaned_data: CleanedDataCreate, db: Session = Depends(get_db)):
    return create_cleaned_data(db=db, cleaned_data=cleaned_data)

@app.get("/cleaned_data/", response_model=list[CleanedDataRead])
async def read_cleaned_data(db: Session = Depends(get_db)):
    return get_cleaned_data(db=db)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ethiopian Medical Data API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
