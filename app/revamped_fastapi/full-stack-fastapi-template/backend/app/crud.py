import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Contribution, ContributionCreate, ContributionUpdate, Item, ItemCreate, User, UserCreate, UserUpdate

###########################################
###########################################
### CONTRIBUTIONS
###########################################
###########################################
def create_contribution(*, session: Session, contribution_in: ContributionCreate, owner_id: uuid.UUID) -> Contribution:
    db_contribution = Item.model_validate(contribution_in, update={"owner_id": owner_id})
    session.add(db_contribution)
    session.commit()
    session.refresh(db_contribution)
    return db_contribution


def update_contribution(*, session: Session, db_contribution: Contribution, contribution_in: ContributionUpdate) -> Any:
    contribution_data = contribution_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "idea_text" in contribution_data:
        new_idea_text = contribution_data["idea_text"]
        extra_data["idea_text"] = new_idea_text
    db_contribution.sqlmodel_update(contribution_data, update=extra_data)
    session.add(db_contribution)
    session.commit()
    session.refresh(db_contribution)
    return db_contribution

def get_contribution_by_id(*, session: Session, contribution_id: uuid.UUID) -> User | None:
    statement = select(Contribution).where(Contribution.id == contribution_id)
    # found_contributions = session.exec(statement).all()
    found_contribution = session.exec(statement).first()
    return found_contribution


def get_contributions_by_owner(*, session: Session, owner_id: uuid.UUID) -> User | None:
    statement = select(Contribution).where(Contribution.email == owner_id)
    # found_contributions = session.exec(statement).first()
    found_contributions = session.exec(statement).all()
    return found_contributions

###########################################
###########################################
### USERS
###########################################
###########################################
def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

###########################################
###########################################
### ITEMS
###########################################
###########################################

def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
