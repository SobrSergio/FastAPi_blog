from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog Service"
    DATABASE_URL: str = "postgresql://fastapi:fastapi@db/blog"

    model_config = ConfigDict(env_file=".env") 

settings = Settings()
