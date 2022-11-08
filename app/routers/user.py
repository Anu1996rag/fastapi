from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import database, models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(error))
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with id {id} not found")
    return user
