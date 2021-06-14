import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repository import UserRepository as UserRepository, UserAccountRepository
from ..repository import MTNRepository as MTNRepository
from .. import schemas, oauth2
from ..DataModels.MTN import MTN as mtn
from database import get_db

router = APIRouter(
    prefix='/mtn',
    tags=['MTN Airtime TopUp']
)


@router.post('/top_up')
def top_up(request: schemas.TopUpData, db: Session = Depends(get_db),
           user: schemas.User = Depends(oauth2.get_current_user)):
    user_data = UserRepository.AuthUser(user.email, db)
    user_balance = UserAccountRepository.get_user_balance(user_data.id, 'mtn', db)
    if int(request.price) > int(user_balance):
        raise HTTPException(detail={"status": 'failed', "message": "not enough balance"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    mtn.top_up(request.phone, request.price)
    if mtn.top_up_response['ResponseCode'] == "000":
        UserAccountRepository.update_user_balance(user_data.id, 'mtn', request.price, db)
        result = dict()
        result['transaction_id'] = json.loads(mtn.top_up_response['ProviderResponse'])['TransactionID']
        result['status'] = mtn.top_up_response['ResponseCode']
        MTNRepository.create(request, db, user_data.id, result)
        return result
    raise HTTPException(detail={"status": 'failed', "message": "sorry top up failed"},
                        status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/get_balance')
def top_up(db: Session = Depends(get_db),
           user: schemas.User = Depends(oauth2.get_current_user)):
    user_data = UserRepository.AuthUser(user.email, db)
    user_balance = UserAccountRepository.get_user_balance(user_data.id, 'mtn', db)
    return user_balance
