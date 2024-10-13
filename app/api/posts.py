import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    logger.info("Создание нового поста")
    try:
        db_post = models.Post(**post.model_dump())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        likes_count = 0
        logger.info(f"Пост создан с id: {db_post.id}")
        return {
            "id": db_post.id,
            "title": db_post.title,
            "content": db_post.content,
            "likes": likes_count
        }
    except Exception as e:
        logger.error(f"Ошибка при создании поста: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка создания поста")

@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    logger.info(f"Обновление поста с id: {post_id}")
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        logger.warning(f"Пост с id: {post_id} не найден")
        raise HTTPException(status_code=404, detail="Пост не найден")
    try:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)

        likes_count = db.query(models.Like).filter(models.Like.post_id == post_id).count()
        logger.info(f"Пост с id: {db_post.id} успешно обновлён")
        return {
            "id": db_post.id,
            "title": db_post.title,
            "content": db_post.content,
            "likes": likes_count
        }
    except Exception as e:
        logger.error(f"Ошибка при обновлении поста: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка обновления поста")


@router.delete("/{post_id}", response_model=schemas.PostResponse)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Удаление поста с id: {post_id}")
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        logger.warning(f"Пост с id: {post_id} не найден")
        raise HTTPException(status_code=404, detail="Пост не найден")
    try:
        db.delete(db_post)
        db.commit()
        logger.info(f"Пост с id: {post_id} успешно удалён")
        return {
            "id": db_post.id,
            "title": db_post.title,
            "content": db_post.content,
            "likes": 0  
        }
    except Exception as e:
        logger.error(f"Ошибка при удалении поста: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка удаления поста")

@router.get("/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Получение поста с id: {post_id}")
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        logger.warning(f"Пост с id: {post_id} не найден")
        raise HTTPException(status_code=404, detail="Пост не найден")

    
    likes_count = db.query(models.Like).filter(models.Like.post_id == post_id).count()
    
    return {
        "id": db_post.id,
        "title": db_post.title,
        "content": db_post.content,
        "likes": likes_count  
    }

@router.get("/", response_model=list[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Получение списка постов с пропуском {skip} и лимитом {limit}")
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    
    
    response_posts = []
    for post in posts:
        likes_count = db.query(models.Like).filter(models.Like.post_id == post.id).count()
        response_posts.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "likes": likes_count
        })
    
    return response_posts
