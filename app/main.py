from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import employees, attendance

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    employees.router, 
    prefix=f"{settings.API_V1_STR}/employees", 
    tags=["Employees"]
)

app.include_router(
    attendance.router, 
    prefix=f"{settings.API_V1_STR}/attendance", 
    tags=["Attendance"]
)

@app.get("/")
def root():
    return {"message": "HRMS Lite API is live"}