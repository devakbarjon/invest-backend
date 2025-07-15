from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, BigInteger
from sqlalchemy.sql import func

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)  # Optional description
    chat_id = Column(BigInteger, nullable=False)  # Chat ID for the task
    link = Column(String, nullable=False)
    icon = Column(String, nullable=True)  # Optional icon URL
    pin = Column(Boolean, default=True)  # Indicates if the task is pinned
    type = Column(String, nullable=False)  # e.g., 'main', 'partner'
    status = Column(Boolean, default=True)
    users = Column(ARRAY(BigInteger), default=[])  # List of user IDs who complated the task
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(
            self, 
            name: str, 
            link: str, 
            type: str, 
            description: str = None, 
            icon: str = None, 
            pin: bool = True
            ):
       
        self.name = name
        self.link = link
        self.type = type
        self.description = description
        self.icon = icon
        self.pin = pin

    def __repr__(self):
        return f"<Task(id={self.id}, status={self.status})>"