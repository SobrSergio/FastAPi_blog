from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PostCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=5000)

class PostUpdate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=5000)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    likes: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
