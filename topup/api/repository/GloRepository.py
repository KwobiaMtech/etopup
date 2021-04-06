from sqlalchemy.orm import Session
from api import models, schemas
from typing import Optional
from fastapi import HTTPException, status


def create(request: schemas.TopUpData, db: Session, user_id, result: Optional[dict]):
    top_up = models.Glo(
        price=request.price,
        phone=request.phone,
        user_id=user_id,
        reference=result["reference"],
        status=result["status"],
        description=result["description"],
        balance=result["balance"],
    )
    db.add(top_up)
    db.commit()
    db.refresh(top_up)
    return top_up


