from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, models, oauth2, schemas, utils
from logger import logger

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        logger.info("User not found")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        logger.info("Invalid credentials entered")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    logger.info(f"Token generated for user {user_credentials.username}")
    return {"token_type": "bearer", "access_token": access_token}

