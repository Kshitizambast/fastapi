from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session



import models
from schemas import *
from database import get_db
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
    return {"data": post}

# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: models.Post, db: Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     return {"data": post}

#create post

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



# update post
@router.put("/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post

# delete post
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}