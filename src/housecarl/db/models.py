# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the database models.

"""

from datetime import UTC, datetime, timedelta

import enum

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Interval,
    String,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class InspectionState(enum.Enum):
    """
    Specifies the possible inspection states.

    """
    Unknown   = 0
    Critical  = 1
    Poor      = 2
    Fair      = 3
    Good      = 4
    Excellent = 5


class Base(DeclarativeBase):
    """
    Base class for all application database models.

    """
    pass


class Room(Base):
    """
    Database model for a room or area in a house.

    """

    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String)

    tasks: Mapped[list[Task]] = relationship(
        back_populates='room',
        cascade='all, delete-orphan',
    )


class Task(Base):
    """
    Database model for tasks.

    """

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str|None] = mapped_column(
        String,
        nullable=True,
        default=None,
    )

    frequency: Mapped[timedelta] = mapped_column(Interval, nullable=False)

    state: Mapped[InspectionState] = mapped_column(
        Enum(InspectionState),
        nullable=False,
    ) 

    last_performed: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    last_inspected: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False,
        index=True,
    )

    room: Mapped[Room] = relationship(back_populates='tasks')


if __name__ == '__main__':
    pass

