from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from src.database import Base
from datetime import datetime


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)

    task_executor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)


