from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    employee_id: str  
    full_name: str
    email: EmailStr            
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int  

    model_config = ConfigDict(from_attributes=True)