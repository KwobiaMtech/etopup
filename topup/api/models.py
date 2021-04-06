from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

from database import Base


class Vodafone(Base):
    __tablename__ = 'vodafone'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    ref = Column(String, nullable=True)
    status = Column(String, nullable=True)

    creator = relationship("User", back_populates="vodafone")


class Glo(Base):
    __tablename__ = 'glo'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    phone = Column(String)
    reference = Column(String, nullable=True)
    status = Column(String, nullable=True)
    description = Column(String, nullable=True)
    balance = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="glo")
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    password = Column(String)

    user_account = relationship('UserAccount', back_populates="creator")
    vodafone = relationship('Vodafone', back_populates="creator")
    glo = relationship('Glo', back_populates="creator")
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Integer)
    net_work = Column(String)
    is_active = Column(Boolean, default=True)

    creator = relationship("User", back_populates="user_account")
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
