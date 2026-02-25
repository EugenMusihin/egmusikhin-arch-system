from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from models import DevelopmentPlan, Goal
from schemas import PlanSchema, PlanCreateSchema, GoalSchema
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="Employee Development Plans API")

Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        if not db.query(DevelopmentPlan).first():
            plans = [
                DevelopmentPlan(id=1, employee_id=1, title='Plan 1', status='active'),
                DevelopmentPlan(id=2, employee_id=2, title='Plan 2', status='completed'),
                DevelopmentPlan(id=3, employee_id=3, title='Plan 3', status='active'),
                DevelopmentPlan(id=4, employee_id=4, title='Plan 4', status='draft'),
                DevelopmentPlan(id=5, employee_id=5, title='Plan 5', status='active'),
                DevelopmentPlan(id=6, employee_id=6, title='Plan 6', status='completed'),
                DevelopmentPlan(id=7, employee_id=7, title='Plan 7', status='draft'),
                DevelopmentPlan(id=8, employee_id=8, title='Plan 8', status='active'),
                DevelopmentPlan(id=9, employee_id=9, title='Plan 9', status='active'),
                DevelopmentPlan(id=10, employee_id=10, title='Plan 10', status='completed')
            ]
            db.add_all(plans)
            db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/plans", response_model=List[PlanSchema])
def get_plans(db: Session = Depends(get_db)):
    return db.query(DevelopmentPlan).all()

@app.get("/api/plans/{plan_id}", response_model=PlanSchema)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(DevelopmentPlan).filter(DevelopmentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@app.post("/api/plans", response_model=PlanSchema, status_code=201)
def create_plan(plan: PlanCreateSchema, db: Session = Depends(get_db)):
    db_plan = DevelopmentPlan(
        employee_id=plan.employee_id,
        title=plan.title,
        status=plan.status
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@app.put("/api/plans/{plan_id}", response_model=PlanSchema)
def update_plan(plan_id: int, plan: PlanCreateSchema, db: Session = Depends(get_db)):
    db_plan = db.query(DevelopmentPlan).filter(DevelopmentPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db_plan.employee_id = plan.employee_id
    db_plan.title = plan.title
    db_plan.status = plan.status
    db.commit()
    db.refresh(db_plan)
    return db_plan

@app.delete("/api/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(DevelopmentPlan).filter(DevelopmentPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
    return {"message": "План успешно удален"}

@app.get("/api/plans/{plan_id}/goals", response_model=List[GoalSchema])
def get_goals(plan_id: int, db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.plan_id == plan_id).all()
