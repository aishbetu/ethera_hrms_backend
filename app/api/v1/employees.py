from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, Employee as EmployeeSchema

router = APIRouter()

@router.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(
        Employee.employee_id == employee.employee_id
    ).first()
    if db_employee:
        raise HTTPException(
            status_code=400, 
            detail="Employee ID already exists"
        )
    
    db_email = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_email:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )

    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/", response_model=List[EmployeeSchema])
def read_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.delete("/{emp_id_str}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id_str: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == emp_id_str).first()
    if not employee:
        raise HTTPException(
            status_code=404, 
            detail=f"Employee with ID {emp_id_str} not found"
        )
    db.delete(employee)
    db.commit()
    return None