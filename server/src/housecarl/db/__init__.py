# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Handles interfacing with the application database.

"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from housecarl.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session]:
    """
    Yields a database session.

    """
    with SessionLocal() as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]


if __name__ == "__main__":
    pass
