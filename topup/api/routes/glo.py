from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.repository import UserRepository as UserRepository
from api.repository import GloRepository, UserAccountRepository
from api import schemas, oauth2
from api.QueryApis.Glo import Glo as glo
from database import get_db

router = APIRouter(
    prefix='/glo',
    tags=['GLO TopUp']
)


@router.post('/top_up')
def top_up(request: schemas.TopUpData, db: Session = Depends(get_db),
           user: schemas.User = Depends(oauth2.get_current_user)):
    user_data = UserRepository.AuthUser(user.email, db)
    user_balance = UserAccountRepository.get_user_balance(user_data.id, 'glo', db)
    if int(request.price) > int(user_balance):
        raise HTTPException(detail={"status": 'failed', "message": "not enough balance"}, status_code=status.HTTP_400_BAD_REQUEST)
    result = glo.topup(request.price, request.phone)
    if result["status"] == "0":
        UserAccountRepository.update_user_balance(user_data.id, 'glo', request.price, db)
    GloRepository.create(request, db, user_data.id, result)
    return result
