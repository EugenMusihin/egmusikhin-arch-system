from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from models import DevelopmentPlan, Goal
from schemas import PlanSchema, PlanCreateSchema, GoalSchema

app = FastAPI(title="Employee Development Plans API")
Base.metadata.create_all(bind=engine)

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

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database not ready")