from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.services.user_services import UserService, UserConflictError
from app.schemas.user_schemas import (
    UserCreateSchema,
    UserGetSchema,
    UserUpdateSchema
)

from app.core.logging import get_logger
logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserGetSchema, status_code=status.HTTP_201_CREATED)
def create(
    user: UserCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new user.

    Args:
        user: The request body with user creation data.
        db: The database session injected by FastAPI.

    Returns:
        The created user data.

    Raises:
        HTTPException: 409 if email or phone already exists.
    """
    try:
        result = UserService(db).create(
            user=user
        )
    except UserConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return result


@router.get("/{id}", response_model=UserGetSchema)
def get(
    id: UUID,
    db: Session = Depends(get_db)
):
    """Retrieve a user by ID.

    Args:
        id: The UUID of the user to retrieve.
        db: The database session injected by FastAPI.

    Returns:
        The user data.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    user = UserService(db).get(id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=List[UserGetSchema])
def list_(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all users with optional search filter.

    Args:
        search: Optional text to filter users by name, email, or phone.
        db: The database session injected by FastAPI.

    Returns:
        A list of user data.
    """
    return UserService(db).list(
        search=search
    )


@router.put("/{id}", response_model=UserGetSchema)
def update(
    id: UUID,
    user: UserUpdateSchema,
    db: Session = Depends(get_db)
):
    """Update an existing user's data.

    Args:
        id: The UUID of the user to update.
        user: The request body with fields to update.
        db: The database session injected by FastAPI.

    Returns:
        The updated user data.

    Raises:
        HTTPException: 404 if the user is not found, 409 if email or phone conflicts.
    """
    try:
        result = UserService(db).update(
            id=id,
            user=user
        )
    except UserConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a user by ID.

    Args:
        id: The UUID of the user to delete.
        db: The database session injected by FastAPI.

    Returns:
        No content on success.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    result = UserService(db).delete(id=id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
