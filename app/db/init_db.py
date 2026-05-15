from app.db.database import engine
from app.db.models import Base


def initialize_database():
    """
    Creates all database tables.
    """

    Base.metadata.create_all(bind=engine)