from http.client import HTTPException
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path
from sqlalchemy import text
from app import crud, schemas,models
from sqlalchemy import func


from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="MIS_Tasks")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Startup event for DB connection test
@app.on_event("startup")
def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Connected to SQL Server successfully.")
    except SQLAlchemyError as e:
        print("❌ Failed to connect to SQL Server:", str(e))
    finally:
        db.close()

# ✅ Dependency for injecting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Read endpoint
@app.get("/mis", response_model=list[schemas.MIS])
def read_mis_entries(db: Session = Depends(get_db)):
    return crud.get_all_mis(db)

@app.post("/mis", response_model=schemas.MIS)
def create_mis_entry(mis: schemas.MISCreate, db: Session = Depends(get_db)):
    return crud.create_mis(db, mis)

@app.get("/mis/count")
def get_mis_count(db: Session = Depends(get_db)):
    count = db.query(models.MIS_Table).count()
    return {"total_mis": count}

@app.get("/mis/all")
def get_all_mis_records(db: Session=Depends(get_db)):
    records= db.query(models.MIS_Table).all()
    return {'records': records}

@app.get("/mis/status-count")
def get_status_count(status: str, db: Session= Depends(get_db)):
    count = db.query(models.MIS_Table).filter(
        func.lower(func.trim(models.MIS_Table.mis_status)) == status.strip().lower()
    ).count()
    return {"status": status, "count":count}

@app.put("/mis/update/{mis_id}")
def update_mis_recor(mis_id: int, updated_data: schemas.MISUpdateSchema, db: Session=Depends(get_db)):
    record=db.query(models.MIS_Table).filter(models.MIS_Table.mis_no==mis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(record,key,value)
    db.commit()
    db.refresh(record)
    return {"message": "Record updated successfully", "record": record}

@app.delete("/mis/delete/{mis_id}")
def delete_mis_record(mis_id: int= Path(...), db: Session=Depends(get_db)):
    record= db.query(models.MIS_Table).filter(models.MIS_Table.mis_no==mis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"message": f"MIS record {mis_id} deleted successfully"}

@app.get("/resources", response_model=list[schemas.TeamOut])
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()