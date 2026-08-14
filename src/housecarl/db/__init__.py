# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Handles interfacing with the application database.

"""

from typing import Annotated, Generator

from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from housecarl.db.models import Base


DATABASE_URL = "sqlite:///housecarl.db"

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session]:
    """
    Yields a database session.

    """
    with SessionLocal() as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]


def initialize():
    """
    Initializes the application database.

    """
    # TODO: This should be handled by migrations using a something like
    #       [Alembic](https://alembic.sqlalchemy.org/en/latest/)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass

