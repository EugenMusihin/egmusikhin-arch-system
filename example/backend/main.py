from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, Base
from models import DevelopmentPlan, Goal
from schemas import PlanSchema, PlanCreateSchema, GoalSchema

app = FastAPI(title="Employee Development Plans API")

Base.metadata.create_all(bind=engine)
import time
from sqlalchemy.exc import OperationalError

def wait_for_db(max_attempts=10, wait_seconds=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            from database import engine
            conn = engine.connect()
            conn.close()
            print("Database is ready")
            return
        except OperationalError:
            attempts += 1
            print(f"Waiting for DB ({attempts}/{max_attempts})...")
            time.sleep(wait_seconds)
    raise Exception("Database not ready after waiting")

wait_for_db()
def init_db_safe():
    db = SessionLocal()
    try:
        if not db.query(DevelopmentPlan).first():
            plans = [
                DevelopmentPlan(id=i, employee_id=i, title=f'Plan {i}', status='active' if i % 3 != 0 else 'completed')
                for i in range(1, 11)
            ]
            db.bulk_save_objects(plans)
            db.commit()

            db.execute("SELECT setval(pg_get_serial_sequence('plans','id'), (SELECT MAX(id) FROM plans));")
            db.commit()
    except Exception as e:
        print("DB init error:", e)
        db.rollback()
    finally:
        db.close()

init_db_safe()

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