from __future__ import annotations
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select, or_
from app.infrastructure.database.repository.base_repository import Repository
from app.models.user_models import UserModel


class UserRepository(Repository):

    def create(self, user: UserModel) -> UserModel:
        """Persist a new user in the database.

        Args:
            user: The UserModel instance to be created.

        Returns:
            The persisted UserModel instance.
        """
        self.db.add(user)
        self.db.flush()
        return user

    def get(self, **filters) -> UserModel | None:
        """Retrieve a single user matching the given filters.

        Args:
            **filters: Keyword arguments used as column-level equality filters.

        Returns:
            The matching UserModel instance, or None if not found.
        """
        return self.db.query(UserModel).filter_by(**filters).first()

    def get_by_email(self, email: EmailStr) -> UserModel | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The matching UserModel instance, or None if not found.
        """
        return self.db.query(UserModel).filter_by(email=email).first()

    def get_by_phone(self, phone: str) -> UserModel | None:
        """Retrieve a user by their phone number.

        Args:
            phone: The phone number to search for.

        Returns:
            The matching UserModel instance, or None if not found.
        """
        return self.db.query(UserModel).filter_by(phone=phone).first()

    def list(self, search: str | None = None, **filters) -> list[UserModel]:
        """List users with optional text search and filters.

        Args:
            search: Optional search string matched against email, phone,
                first_name, and last_name using case-insensitive LIKE.
            **filters: Keyword arguments used as column-level equality filters.

        Returns:
            A list of UserModel instances matching the criteria.
        """
        statement = select(UserModel).filter_by(**filters)

        if search:
            search_pattern = f"%{search}%"
            statement = statement.filter(
                or_(
                    UserModel.email.ilike(search_pattern),
                    UserModel.phone.ilike(search_pattern),
                    UserModel.first_name.ilike(search_pattern),
                    UserModel.last_name.ilike(search_pattern),
                )
            )

        return list(self.db.scalars(statement).all())


    def update(self, id: UUID,  **updated_fields) -> UserModel | None:
        """Update an existing user's fields by ID.

        Args:
            id: The UUID of the user to update.
            **updated_fields: Key-value pairs of fields to update.

        Returns:
            The updated UserModel instance, or None if the user was not found.
        """
        user = self.get(id=id)
        if not user:
            return None

        for key, value in updated_fields.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.db.flush()
        return user

    def delete(self, id: UUID) -> UserModel | None:
        """Delete a user by ID.

        Args:
            id: The UUID of the user to delete.

        Returns:
            The deleted UserModel instance, or None if the user was not found.
        """
        user = self.get(id=id)
        if not user:
            return None

        self.db.delete(user)
        self.db.flush()
        return user
