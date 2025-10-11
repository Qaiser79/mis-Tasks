from app.models import Team, TeamRole  # assuming TeamRole is defined as an Enum

from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path, HTTPException, Query
from sqlalchemy import text, extract
from app import crud, schemas,models
from sqlalchemy import func
from collections import defaultdict
from passlib.context import CryptContext
from typing import Optional

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login")
def login(data: schemas.Loginrequest,db: Session=Depends(get_db)):
    user = db.query(models.Team).filter(models.Team.name == data.username).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"team_id": user.id, "role": user.role}

def get_team_by_id(team_id: int= Query(...), db: Session=Depends(get_db))-> models.Team:
    team= db.query(models.Team).filter(models.Team.id==team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

def require_manager(team: models.Team=Depends(get_team_by_id)):
    if team.role!="admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return team
def require_editor_or_manager(team: models.Team=Depends(get_team_by_id)):
    if team.role not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return team

# ✅ Read endpoint
@app.get("/mis", response_model=list[schemas.MIS])
def read_mis_entries(team_id: int = Query(...), db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.role not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_all_mis(db)

@app.post("/mis", response_model=schemas.MIS)
def create_mis_entry(mis: schemas.MISCreate, db: Session = Depends(get_db), team:models.Team=Depends(require_manager)):
    return crud.create_mis(db, mis)

@app.get("/mis/count")
def get_mis_count(db: Session = Depends(get_db)):
    count = db.query(models.MIS_Table).count()
    return {"total_mis": count}

@app.get("/mis/all")
def get_all_mis_records(team_id: Optional[int]=Query(None),db: Session=Depends(get_db)):
    query=db.query(models.MIS_Table)
    if team_id is not None:
        query=query.filter(models.MIS_Table.resource==team_id)
    records= query.all()
    return {'records': records}

@app.get("/mis/status-count")
def get_status_count(status: str,team_id: Optional[int] = Query(None), db: Session= Depends(get_db)):
    query = db.query(models.MIS_Table).filter(
        func.lower(func.trim(models.MIS_Table.mis_status)) == status.strip().lower()
    )
    if team_id is not None:
        query=query.filter(models.MIS_Table.resource == team_id)
    count=query.count()

    return {"status": status, "count":count}

@app.put("/mis/update/{mis_id}")
def update_mis_recor(mis_id: int, updated_data: schemas.MISUpdateSchema, db: Session=Depends(get_db), team: models.Team = Depends(get_team_by_id)):
    record=db.query(models.MIS_Table).filter(models.MIS_Table.mis_no==mis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    updates= updated_data.dict(exclude_unset=True)
    if team.role=='editor':
        allowed_fields={"mis_status","completed_date","last_uat_date" ,"comment"}
        for field in updates:
            if field not in allowed_fields:
                raise HTTPException(
                    status_code=403,
                    detail=f"Editors cannot update '{field}'"
                )
    for key, value in updates.items():
        setattr(record,key,value)
    db.commit()
    db.refresh(record)
    return {"message": "Record updated successfully", "record": record}

@app.delete("/mis/delete/{mis_id}")
def delete_mis_record(mis_id: int= Path(...), db: Session=Depends(get_db), team: models.Team = Depends(require_manager)):
    record= db.query(models.MIS_Table).filter(models.MIS_Table.mis_no==mis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"message": f"MIS record {mis_id} deleted successfully"}

@app.get("/resources", response_model=list[schemas.TeamOut])
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()

@app.get("/mis/monthly-count")
def get_monthly_count(db: Session = Depends(get_db)):
    monthly_count= defaultdict(int)
    records= db.query(models.MIS_Table.arrival_date).all()
    for record in records:
        if record.arrival_date:
            month= record.arrival_date.strftime('%B')
            monthly_count[month]+=1
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    sorted_counts ={month: monthly_count.get(month,0) for month in month_order}

    return sorted_counts

@app.get("/mis/by-resource")
def get_resource_mis(month: str, db: Session=Depends(get_db)):
    resource_count= defaultdict(int)

    query=db.query(models.MIS_Table.resource, models.MIS_Table.assigned_date)
    if month: 
        query= query.filter(extract('month', models.MIS_Table.assigned_date)==int(month))
    records= query.all()
    for resource, assigned_date in records:
        if resource:
            resource_count[resource]+=1
    return dict(resource_count)

'''@app.get("/mis/by_type")
def get_type_mis(month: int, db: Session=Depends(get_db)):
    type_count= defaultdict(int)
    query= db.query(models.MIS_Table.mis_type, models.MIS_Table.arrival_date)

    if month:
        query= query.filter(extract('month', models.MIS_Table.arrival_date)==int(month))
    records= query.all()

    for mis_type, arrival_date in records:
        if mis_type:
            type_count[mis_type]+=1
    return dict(type_count)'''
@app.get("/mis/type_daily_trend")
def get_type_daily_trend(month: int, db: Session=Depends(get_db)):
    daily_trend=defaultdict(lambda: defaultdict(int))
    query= db.query(models.MIS_Table.mis_type, models.MIS_Table.arrival_date)
    query= query.filter(extract('month',models.MIS_Table.arrival_date)==month)
    records=query.all()

    for mis_type, arrival_date in records:
        if mis_type and arrival_date:
            day_str = arrival_date.strftime('%Y-%m-%d')
            daily_trend[mis_type][day_str]+=1

    return daily_trend

@app.get("/mis/recent/{team_id}")
def get_recent_mis(team_id: int, db: Session=Depends(get_db)):
    records=(db.query(models.MIS_Table)
             .filter(models.MIS_Table.resource==team_id)
             .limit(5)
             .all()
             )
    return {"records": records or []}
