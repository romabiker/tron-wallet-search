import uuid
from sqlalchemy import Integer, func, BigInteger, Float

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from pydantic import EmailStr, BaseModel
from sqlmodel import Field, Relationship, SQLModel

from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlmodel import Session, create_engine, select
from sqlalchemy.ext.asyncio import AsyncAttrs #async_sessionmaker, create_async_engine

from app.core.base_class import Base, AsyncBase


class TimeStampedBase(AsyncBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class IdBase(AsyncBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(IdBase, TimeStampedBase):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    full_name: Mapped[str | None] = mapped_column()


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None

 
class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class TronWallet(IdBase, TimeStampedBase):
    address: str = Field(min_length=1, max_length=255, unique=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


