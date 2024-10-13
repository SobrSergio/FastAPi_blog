import logging
from fastapi import FastAPI
from app.api import posts, likes
from app.db.session import engine
from app.db.base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Таблицы базы данных успешно созданы.")
except Exception as e:
    logger.error(f"Ошибка при создании таблиц базы данных: {e}")

app.include_router(posts.router, prefix="/posts", tags=["Посты"])
app.include_router(likes.router, prefix="/posts/{post_id}/likes", tags=["Лайки"])

@app.get("/")
def read_root():
    logger.info("Доступ к корневой точке API.")
    return {"message": "Добро пожаловать в API сервиса блога"}
