from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Post(Base):
    __tablename__ = 'posts'

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(100), nullable=False)
    content: str = Column(Text, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    
    likes = relationship("Like", back_populates="post", cascade="all, delete") 
