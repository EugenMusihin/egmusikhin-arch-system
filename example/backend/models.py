from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DevelopmentPlan(Base):
    __tablename__ = "development_plan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)

    goals = relationship(
        "Goal",
        back_populates="plan",
        cascade="all, delete-orphan"
    )

class Goal(Base):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("development_plan.id"), nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)

    plan = relationship("DevelopmentPlan", back_populates="goals")
