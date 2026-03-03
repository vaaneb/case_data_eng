from sqlalchemy.orm import Session

class Repository:
    def __init__(self, db: Session):
        """Initialize the repository with a database session.

        Args:
            db: The SQLAlchemy session for database operations.
        """
        self.db = db

    def add(self, model):
        """Add an entity to the session.

        Args:
            model: The ORM model instance to add.

        Returns:
            The added model instance.
        """
        self.db.add(model)
        return model

    def remove(self, model):
        """Mark an entity for deletion from the session.

        Args:
            model: The ORM model instance to delete.
        """
        self.db.delete(model)

    def commit(self):
        """Commit the current transaction."""
        self.db.commit()

    def flush(self):
        """Flush pending changes to the database without committing."""
        self.db.flush()

    def refresh(self, model):
        """Reload an entity's attributes from the database.

        Args:
            model: The ORM model instance to refresh.

        Returns:
            The refreshed model instance.
        """
        self.db.refresh(model)
        return model