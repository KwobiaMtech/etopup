from sqlalchemy.orm import Session
from api import models, schemas
from fastapi import HTTPException, status
from api.hashing import Hash


def get_user_account(user_id, network, db: Session):
    return db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id,
                                               models.UserAccount.net_work == network).first()


def get_user_balance(user_id, network, db: Session):
    user_account = get_user_account(user_id, network, db)
    if not user_account:
        raise HTTPException(detail="Top Up Account not available", status_code=status.HTTP_400_BAD_REQUEST)
    return user_account.balance


def update_user_balance(user_id, network, price, db: Session):
    user_account = get_user_account(user_id, network, db)
    balance = int(user_account.balance) - int(price)
    user_account.balance = balance
    db.commit()
