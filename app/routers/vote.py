from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session

import database
import models
import oauth2
import schemas

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteResponse, db: Session = Depends(database.get_db),
         current_user=Depends(oauth2.get_current_user)):

    # precheck if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)

    found = vote_query.first()
    if vote.dir == 1:
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{current_user.id} has already voted on post {vote.post_id}")

        # add new entry to the votes table
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Vote successfully added !"}
    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        # delete the entry
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Vote successfully deleted !"}
