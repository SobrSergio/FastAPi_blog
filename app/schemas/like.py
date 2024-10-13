from pydantic import BaseModel, ConfigDict

class LikeResponse(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)