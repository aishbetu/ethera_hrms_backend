from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate, Attendance as AttendanceSchema

router = APIRouter()

@router.post("/", response_model=AttendanceSchema, status_code=status.HTTP_201_CREATED)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == attendance.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=404, 
            detail="Employee not found"
        )
    
    existing = db.query(Attendance).filter(
        Attendance.employee_id == attendance.employee_id,
        Attendance.date == attendance.date
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Attendance already marked for {attendance.date}"
        )

    new_record = Attendance(**attendance.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/", response_model=List[AttendanceSchema])
def get_attendance(
    employee_id: Optional[int] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Attendance)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
        
    return query.all()

@router.get("/summary")
def get_attendance_summary(db: Session = Depends(get_db)):
    summary = db.query(
        Attendance.employee_id,
        func.count(Attendance.id).label("total_present")
    ).filter(Attendance.status == "Present").group_by(Attendance.employee_id).all()

    return [{"employee_id": s[0], "present_days": s[1]} for s in summary]