# ==============================================================================
# Copyright (c) 2025 Kevin Fisher
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/>.
# ==============================================================================
"""
"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, SQLModel, Session, create_engine

class Room(SQLModel, table=True):
    """
    Database model for a room.

    """
    id: int = Field(
        description='The room\'s unique identifier.',
        primary_key=True
    )
    name: str = Field(
        description='The room\'s name.',
        index=True,
        unique=True,
    )

# TODO: The database connection string should probably be configurable.
engine = create_engine(
    'sqlite:///database.db', 
    connect_args={'check_same_thread': False}
)

# TODO: Eventually, this should be handled by migrations using something 
#       like Alembic.
def create_db_and_tables():
    """
    Creates the database and tables if they do not exist.
    
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Yields the database session.

    """
    with Session(engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]

if __name__ == '__main__':
    pass
