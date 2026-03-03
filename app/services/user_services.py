from __future__ import annotations
from uuid import UUID
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema
from app.models.user_models import UserModel
from app.infrastructure.security.hash import hash_password

class UserConflictError(Exception):
    """Raised when a unique user field already exists."""
    pass

class EmailConflictError(UserConflictError):
    """Raised when a user email already exists."""
    pass

class PhoneConflictError(UserConflictError):
    """Raised when a user phone already exists."""
    pass

class UserService:
    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db: The SQLAlchemy session used for database operations.
        """
        self.db = db
        self.repository = UserRepository(db)

    def create(
            self,
            user: UserCreateSchema,
            commit: bool = True
    ) -> UserGetSchema:
        """Create a new user after validating email and phone uniqueness.

        Args:
            user: Schema containing the new user's data.
            commit: Whether to commit the transaction. Defaults to True.

        Returns:
            The created user data as a UserGetSchema.

        Raises:
            EmailConflictError: If the email is already registered.
            PhoneConflictError: If the phone is already registered.
        """
        # Check for email conflict
        if self.repository.get_by_email(user.email):
            raise EmailConflictError("Email already registered")

        if self.repository.get_by_phone(user.phone):
            raise PhoneConflictError("Phone already registered")

        user_model = UserModel(
            **user.model_dump(exclude={'password'}),
            hashed_password=hash_password(user.password)
        )

        created_user = self.repository.create(user_model)

        if commit:
            self.db.commit()

        return UserGetSchema.model_validate(created_user)

    def get(self, **kwargs) -> UserGetSchema | None:
        """Retrieve a single user by the given filters.

        Args:
            **kwargs: Keyword arguments used as column-level equality filters.

        Returns:
            The matching user as a UserGetSchema, or None if not found.
        """
        user = self.repository.get(**kwargs)
        if not user:
            return None
        return UserGetSchema.model_validate(user)

    def list(self, search: str | None = None, **kwargs) -> list[UserGetSchema]:
        """List users with optional text search.

        Args:
            search: Optional search string for filtering results.
            **kwargs: Additional column-level equality filters.

        Returns:
            A list of users as UserGetSchema instances.
        """
        users = self.repository.list(search=search, **kwargs)
        return [UserGetSchema.model_validate(user) for user in users]

    def update(
            self,
            id: UUID,
            user: UserUpdateSchema,
    ) -> UserGetSchema | None:
        """Update a user's data, validating email and phone uniqueness.

        Args:
            id: The UUID of the user to update.
            user: Schema containing the fields to update.

        Returns:
            The updated user as a UserGetSchema, or None if not found.

        Raises:
            EmailConflictError: If the new email is already taken by another user.
            PhoneConflictError: If the new phone is already taken by another user.
        """
        existing = self.repository.get(id=id)
        if not existing:
            return None

        update_data = user.model_dump(exclude_unset=True)

        if "email" in update_data:
            conflicting_user = self.repository.get_by_email(update_data["email"])
            if conflicting_user and conflicting_user.id != id:
                raise EmailConflictError("Email already registered")

        if "phone" in update_data:
            conflicting_user = self.repository.get_by_phone(update_data["phone"])
            if conflicting_user and conflicting_user.id != id:
                raise PhoneConflictError("Phone already registered")

        updated_user = self.repository.update(id, **update_data)
        self.db.commit()
        return UserGetSchema.model_validate(updated_user)

    def delete(self, id: UUID) -> UserGetSchema | None:
        """Delete a user by ID.

        Args:
            id: The UUID of the user to delete.

        Returns:
            The deleted user as a UserGetSchema, or None if not found.
        """
        existing = self.repository.get(id=id)
        if not existing:
            return None

        deleted_user = self.repository.delete(id)
        self.db.commit()
        return UserGetSchema.model_validate(deleted_user)
