from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_projects")

    participants = relationship("User", secondary="project_participants", back_populates="participants")



