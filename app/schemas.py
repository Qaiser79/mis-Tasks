from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional

class MIS(BaseModel):
    mis_no: int
    mis_type: Optional[str]
    department: Optional[str]
    arrival_date: Optional[date]
    last_uat_date: Optional[date]
    mis_description: Optional[str]
    mis_status: Optional[str]
    comment: Optional[str]
    completed_date: Optional[date]
    assigned_date: Optional[date]
    target_date: Optional[date]
    resource: Optional[int]
    @validator(
        "arrival_date",
        "last_uat_date",
        "completed_date",
        "assigned_date",
        "target_date",
        pre=True
    )
    def parse_dates(cls, value):
        if value in (None, ""):
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        for fmt in ("%Y-%m-%d", "%d-%b-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
            raise ValueError("Date must be in 'YYYY-MM-DD' or 'DD-MMM-YYYY' format (e.g. '2025-01-10' or '10-Jan-2025')")

class MISCreate(BaseModel):
    mis_no: Optional[int]
    mis_type: Optional[str]
    department: Optional[str]
    arrival_date: Optional[str]
    last_uat_date: Optional[str]
    mis_description: Optional[str]
    mis_status: Optional[str]
    comment: Optional[str]
    completed_date: Optional[str]
    assigned_date: Optional[str]
    target_date: Optional[str]
    resource: Optional[int]

class MISUpdateSchema(BaseModel):
    mis_type: Optional[str]
    department: Optional[str]
    arrival_date: Optional[str]
    last_uat_date: Optional[str]
    mis_description: Optional[str]
    mis_status: Optional[str]
    comment: Optional[str]
    completed_date: Optional[str]
    assigned_date: Optional[str]
    target_date: Optional[str]
    resource: Optional[int]

class TeamOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Config:
    orm_mode = True