# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the API schema.

"""

from datetime import datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from housecarl.db.models import InspectionState


class RoomBase(BaseModel):
    """
    Base room model.

    """

    title: str = Field(
        description="Name of the room.",
    )


class RoomCreate(RoomBase):
    """
    Model used for creating new room entries in the database.

    """


class RoomUpdate(BaseModel):
    """
    Model used for updating an existing room entry in the database.

    Only the fields that are whome have a value provided will be
    updated. All other fields will remain unchanged.
    """

    title: str | None = Field(
        description="Name of the room.",
        default=None,
    )


class RoomItem(RoomBase):
    """
    Model used to get basic information about a room.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="The unique identifier for the room.",
    )


class RoomDetails(RoomBase):
    """
    Model used to get detailed information about a room.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="The unique identifier for the room.",
    )

    tasks: list[TaskDetails] = Field(
        description="List of all tasks associated with the room.",
    )


class TaskBase(BaseModel):
    """
    Base task model.

    """

    title: str = Field(
        description="Brief description or summary of the task.",
    )

    description: str | None = Field(
        description="Detailed description of the task.",
        default=None,
    )

    state: InspectionState = Field(
        description="State of the item associated with the task.",
    )


class TaskCreate(TaskBase):
    """
    Model used when creating new task entries in the database.

    """

    frequency: timedelta = Field(
        description="How often the task is expected to be completed.",
    )

    room_id: int = Field(
        description="Id of the room the task is associated with.",
    )


class TaskUpdate(BaseModel):
    """
    Model used for updating an existing task entry in the database.

    Only the fields that are whome have a value provided will be
    updated. All other fields will remain unchanged.
    """

    title: str | None = Field(
        description="Brief description or summary of the task.",
        default=None,
    )

    description: str | None = Field(
        description="Detailed description of the task.",
        default=None,
    )

    state: InspectionState | None = Field(
        description="State of the item associated with the task.",
        default=None,
    )

    frequency: timedelta | None = Field(
        description="How often the task is expected to be completed.",
        default=None,
    )

    last_performed: datetime | None = Field(
        description="Last time the task was performed.",
        default=None,
    )

    last_inspected: datetime | None = Field(
        description="Last time the state was inspected",
        default=None,
    )

    room_id: int | None = Field(
        description="Id of the room the task is associated with.",
        default=None,
    )


class TaskItem(TaskBase):
    """
    Model used to get basic information about a task.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="The unique identifier for the task.",
    )

    room: RoomItem = Field(
        description="The room the task is associated with.",
    )


class TaskDetails(TaskBase):
    """
    Model used to get detailed information about a task.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="The unique identifier for the task.",
    )

    frequency: timedelta = Field(
        description="How often the task is expected to be completed.",
    )

    last_performed: datetime = Field(
        description="Last time the task was performed.",
    )

    last_inspected: datetime = Field(
        description="Last time the state was inspected",
    )


class RandomTaskGenerate(BaseModel):
    """
    Model used when generating a new set of random tasks.

    """

    count: Literal[4, 6, 12, 20] = Field(
        description="Number of random tasks to generate.",
    )


class RandomTaskItem(BaseModel):
    """
    Model used to get basic information about a random task.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description="The unique identifier for the random task entry.",
    )

    number: int = Field(
        description="Number assigned to the random task.",
    )

    task: TaskItem = Field(
        description="The task selected for this random task entry.",
    )


if __name__ == "__main__":
    pass
