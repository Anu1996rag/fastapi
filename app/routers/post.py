from typing import List, Optional

from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import database, models, oauth2, schemas
from logger import logger

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(database.get_db),
                    current_user=Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    logger.info("Fetching all posts")
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
async def get_posts_by_id(id: int, db: Session = Depends(database.get_db),
                          current_user=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not posts:
        logger.info(f"Post with id {id} not found in the database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with id {id} not found")
    logger.info(f"Post with id {id} fetched from the database")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                       current_user=Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logger.info(f"Post with id {new_post.id} created successfully.")
    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db),
                      current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        logger.info(f"Post with id {id} not found in the database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post.owner_id != current_user.owner_id:
        logger.info(f"Request forbidden as owner id of the post {post.owner_id} "
                    f"does not match with current user {current_user.owner_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Requested action could not be performed.")

    # update the post and commit to the database
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    logger.info(f"Post with id {post_query.first().id} updated successfully.")
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int, db: Session = Depends(database.get_db),
                            current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        logger.info(f"Post with id {id} not found in the database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        logger.info(f"Request forbidden as owner id of the post {post.owner_id} "
                    f"does not match with current user {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Requested action could not be performed.")

    post.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Post with id {id} deleted successfully.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
