import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser, # CurrentUser = Annotated[User, Depends(get_current_user)]
    SessionDep,
    get_current_active_supercontribution,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    Message,
    UpdatePassword,
    Contribution,
    ContributionCreate,
    ContributionPublic,
    ContributionsPublic,
    ContributionUpdate,
)
from app.utils import generate_new_account_email, send_email

router = APIRouter(prefix="/contributions", tags=["contributions"])


@router.get(
    "/",
    response_model=ContributionsPublic,
)
def read_contributions(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve contributions.
    """

    count_statement = select(func.count()).select_from(Contribution)
    count = session.exec(count_statement).one()

    statement = select(Contribution).where(Contribution.owner_id == current_user.id).offset(skip).limit(limit)
    contributions = session.exec(statement).all()

    return ContributionsPublic(data=contributions, count=count)



@router.get("/{contribution_id}", response_model=ContributionPublic)
def read_contribution_by_id(
    contribution_id: uuid.UUID, session: SessionDep
) -> Any:
    """
    Get a specific contribution by id.
    """
    contribution = crud.get_contribution_by_id(session=session, id=contribution_id)# session.get(Contribution, contribution_id)
    return contribution


@router.post(
    "/", dependencies=[Depends(get_current_active_supercontribution)], response_model=ContributionPublic
)
def create_contribution(*, session: SessionDep, current_user: CurrentUser, contribution_in: ContributionCreate) -> Any:
    """
    Create new contribution.
    """

    contribution = crud.create_contribution(session=session, contribution_in=contribution_in, owner_id=current_user.id) # def create_contribution(*, session: Session, contribution_in: ContributionCreate, owner_id: uuid.UUID) -> Contribution:
    return contribution

@router.delete("/{contribution_to_delete_id}", response_model=Message)
def delete_contribution(session: SessionDep, contribution_to_delete_id: uuid.UUID,) -> Any:
    """
    Delete contribution.
    """
    existing_contribution = crud.get_contribution_by_id(session=session, contribution_id=contribution_to_delete_id) # def get_contribution_by_id(*, session: Session, contribution_id: uuid.UUID) -> User | None:
    if existing_contribution:
        session.delete(existing_contribution)
        session.commit()
        return Message(message="Contribution deleted successfully")
    else:
        raise HTTPException(
            status_code=409, detail="Error Deleting: Contribution does not exists"
        )

@router.patch(
    "/{contribution_id}",
    # dependencies=[Depends(get_current_active_supercontribution)],
    response_model=ContributionPublic,
)
def update_contribution(
    *,
    session: SessionDep,
    contribution_id: uuid.UUID,
    contribution_in: ContributionUpdate,
) -> Any:
    """
    Update a contribution.
    """

    db_contribution = session.get(Contribution, contribution_id)
    if not db_contribution:
        raise HTTPException(
            status_code=404,
            detail="The contribution with this id does not exist in the system",
        )
    db_contribution = crud.update_contribution(session=session, db_contribution=db_contribution, contribution_in=contribution_in) # def update_contribution(*, session: Session, db_contribution: Contribution, contribution_in: ContributionUpdate) -> Any:
    return db_contribution
