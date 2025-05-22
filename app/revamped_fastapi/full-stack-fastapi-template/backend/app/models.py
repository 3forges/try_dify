import datetime
from typing import Optional
import uuid

from pydantic import EmailStr
from sqlalchemy import DateTime, func
from sqlmodel import SQLModel, Column, Field, Relationship

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

###########################################
###########################################
### ITEMS
###########################################
###########################################

# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


###########################################
###########################################
### CONTRIBUTIONS
###########################################
###########################################

# Shared properties
class ContributionBase(SQLModel):
    idea_text: str = Field(min_length=1, max_length=510)


# Properties to receive on contribution creation
class ContributionCreate(ContributionBase):
    pass


# Properties to receive on contribution update
class ContributionUpdate(ContributionBase):
    idea_text: str | None = Field(default=None, min_length=1, max_length=510)  # type: ignore


# Database model, database table inferred from class name
class Contribution(ContributionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    idea_text: str = Field(max_length=510)
    created_at: datetime.datetime = Field(
        # default_factory=datetime.datetime.utcnow,
        default_factory=datetime.datetime.now,
    )
    updated_at: Optional[datetime.datetime] = Field(
        # sa_column=Column(DateTime(), onupdate=datetime.datetime.now)
        sa_column=Column(DateTime(), onupdate=func.now())
        
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="contributions")


# Properties to return via API, id is always required
class ContributionPublic(ContributionBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ContributionsPublic(SQLModel):
    data: list[ContributionPublic]
    count: int


###########################################
###########################################
### END  OF CONTRIBUTIONS
###########################################
###########################################




###########################################
###########################################
### END  OF TRANSCRIPTIONS
###########################################
###########################################


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
