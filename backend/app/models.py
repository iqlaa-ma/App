# from sqlalchemy import Column, Integer, String, DateTime, Boolean
# from sqlalchemy.sql import func
# from app.database import Base


# class User(Base):
#     """User model for authentication"""
    
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     username = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
#     def __repr__(self):
#         return f"<User(id={self.id}, email={self.email}, username={self.username})>"

#mongodb
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional
from pymongo import IndexModel
from bson import ObjectId

class User(Document):
    """User model for authentication using MongoDB"""
    
    email: Indexed(str, unique=True)  # Indexed and unique
    username: Indexed(str, unique=True)  # Indexed and unique
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        name = "users"  # Collection name
        indexes = [
            IndexModel([("email", 1)], unique=True),
            IndexModel([("username", 1)], unique=True),
        ]
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
    
    async def save_with_updated_time(self, **kwargs):
        """Save document and update the updated_at field"""
        self.updated_at = datetime.utcnow()
        return await self.save(**kwargs)
    
    def dict(self, **kwargs):
        """Override dict method to convert ObjectId to string"""
        data = super().dict(**kwargs)
        if 'id' in data and isinstance(data['id'], ObjectId):
            data['id'] = str(data['id'])
        return data
    
    class Config:
        # Configure JSON encoding for ObjectId
        json_encoders = {
            ObjectId: str
        }
        use_enum_values = True