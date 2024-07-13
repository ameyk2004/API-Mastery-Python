from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models, oath2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):

    current_user = db.query(models.User).filter(models.User.id == user_id.id).first()

    new_post = models.Post(title = post.title, content=post.content, published=post.published, owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}')
def get_post(id:int, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return {"post" : post}

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  user_id: int = Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to perform this")
    
    post_query.delete(synchronize_session=False)
    db.commit()
  

@router.put('/{id}')
def update_post(id: int, my_post: schemas.Post, db: Session = Depends(get_db),  user_id: int = Depends(oath2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to perform this")
    
    post_query.update({'title' : my_post.title, 'content': my_post.content, 'published' : my_post.published})

    db.commit()

    return {"status" : "success"}
