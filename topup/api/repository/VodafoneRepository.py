from typing import Optional

from sqlalchemy.orm import Session
from api import models, schemas


def create(request: schemas.TopUpData, db: Session, user_id, result: Optional[dict]):
    top_up = models.Vodafone(price=request.price,
                             phone=request.phone,
                             user_id=user_id,
                             ref=result["transaction_id"],
                             status=result["status"]
                             )
    db.add(top_up)
    db.commit()
    db.refresh(top_up)
    return top_up
