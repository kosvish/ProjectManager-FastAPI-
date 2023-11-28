from sqlalchemy import Column, Integer, ForeignKey, JSON, String
from src.database import Base
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)


class ProjectParticipants(Base):
    __tablename__ = 'project_participants'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="participants")

