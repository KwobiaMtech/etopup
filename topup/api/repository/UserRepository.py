from sqlalchemy.orm import Session
from api import models, schemas
from fastapi import HTTPException, status
from api.hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} was not found")
    return user


def AuthUser(email: str, db: Session):
    user_data = db.query(models.User).filter(models.User.email == email).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Validation Error")
    return user_data
