from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from api import schemas
from api.repository import UserRepository

router = APIRouter(
    prefix="/usr",
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return UserRepository.create(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def show(id: int, db: Session = Depends(get_db)):
    return UserRepository.show(id, db)
