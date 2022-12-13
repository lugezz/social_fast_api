from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.oauth2 import get_current_user


router = APIRouter(prefix="/vote", tags=['Vote'])


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def vote_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Vote post
    """
    this_post = db.query(models.Post).get(post_id)
    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Post Id {post_id} not found'})

    # If exists -> delete, if not -> create
    this_vote_qs = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == post_id)

    if this_vote_qs.all():
        this_vote_qs.delete(synchronize_session=False)
        message = 'Vote removed successfully'
    else:
        new_vote = models.Vote(post_id=post_id, user_id=current_user.id)
        message = 'Vote created successfully'
        db.add(new_vote)

    db.commit()

    return {"message": message}
