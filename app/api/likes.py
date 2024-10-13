from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.db.session import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=dict)
def like_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Добавление лайка к посту с id: {post_id}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        logger.warning(f"Пост с id: {post_id} не найден")
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    like = models.Like(post_id=post.id)
    db.add(like)
    db.commit()
    logger.info(f"Лайк успешно добавлен к посту с id: {post_id}")
    return {"message": "Пост лайкнут"}

@router.delete("/", response_model=dict) 
def unlike_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Удаление лайка у поста с id: {post_id}")
    like = db.query(models.Like).filter(models.Like.post_id == post_id).first()
    if not like:
        logger.warning(f"Лайк для поста с id: {post_id} не найден")
        raise HTTPException(status_code=404, detail="Лайк не найден")
    
    db.delete(like)
    db.commit()
    logger.info(f"Лайк успешно удален у поста с id: {post_id}")
    return {"message": "Лайк убран"}
