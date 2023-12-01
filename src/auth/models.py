from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    authenticated = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    created_projects = relationship('Project', back_populates='creator')
    participated_projects = relationship('ProjectParticipants', back_populates='user')


class ProjectParticipants(Base):
    __tablename__ = 'project_participants'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    user = relationship("User", back_populates="participated_projects")
    project = relationship("Project", back_populates="participants")
    role = relationship("Role")


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_projects")
    participants = relationship("ProjectParticipants", back_populates="project")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    task_executor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    executor = relationship("User", foreign_keys=[task_executor_id])
    project = relationship("Project", back_populates="tasks")
