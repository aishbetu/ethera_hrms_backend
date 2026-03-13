from pydantic import BaseModel, ConfigDict
from datetime import date
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatus
    employee_id: int

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)