from pydantic import BaseModel
from datetime import date
from typing import List

class PlanSchema(BaseModel):
    id: int
    employee_id: int
    title: str
    status: str

    class Config:
        orm_mode = True

class PlanCreateSchema(BaseModel):
    employee_id: int
    title: str
    status: str

class GoalSchema(BaseModel):
    id: int
    plan_id: int
    description: str
    deadline: date

    class Config:
        orm_mode = True

class GoalCreateSchema(BaseModel):
    plan_id: int
    description: str
    deadline: date
