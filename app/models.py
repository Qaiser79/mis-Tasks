from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import date


class Team(Base):
    __tablename__="team"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    mis_entries= relationship("MIS_Table", back_populates="resource_team")

class MIS_Table(Base):
    __tablename__="mis_table"
    mis_no = Column(Integer, primary_key=True, index=True,autoincrement=False)
    mis_type = Column(String(50))
    department = Column(String(50))
    arrival_date = Column(Date)
    last_uat_date = Column(Date)
    mis_description = Column(String)  # nvarchar(max)
    mis_status = Column(String(50))
    comment = Column(String(50))
    completed_date = Column(Date)  # Consider changing to Date if possible
    assigned_date = Column(Date)
    target_date = Column(Date)
    resource = Column(Integer, ForeignKey("team.id"))

    resource_team= relationship("Team", back_populates="mis_entries")

