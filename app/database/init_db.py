from app.database.base import Base

from app.database.database import engine

import app.database.models


def init_database():

    Base.metadata.create_all(engine)


if __name__ == "__main__":

    init_database()

    print("Database initialized.")