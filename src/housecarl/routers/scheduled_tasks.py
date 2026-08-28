# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the scheduled tasks endpoint.

"""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from housecarl.db import DatabaseSession
from housecarl.db.models import ScheduledTask
from housecarl.routers.tasks import get_task_or_404
from housecarl.schema import ScheduledTaskItem, ScheduledTaskSchedule


def get_scheduled_task_or_404(task_id: int, db: Session) -> ScheduledTask:
    """
    Returns a scheduled task entry from the database.

    Args:
        task_id:
            Unique identifier for the task the schedule entry belongs to.
        db:
            Database session to use when performing database operations.

    Raises:
        HTTPException:
            Raised if the task is not currently scheduled.

    """
    scheduled_task = db.execute(
        select(ScheduledTask).where(ScheduledTask.task_id == task_id)
    ).scalar_one_or_none()
    if scheduled_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled task not found",
        )
    return scheduled_task


def start_of_day(moment: datetime) -> datetime:
    """
    Returns the start of the UTC day containing the given moment.

    """
    return moment.astimezone(UTC).replace(hour=0, minute=0, second=0, microsecond=0)


router = APIRouter()


@router.get("", response_model=list[ScheduledTaskItem])
def all(db: DatabaseSession):
    """
    Returns list of all scheduled tasks, sorted by date.

    """
    return (
        db.execute(select(ScheduledTask).order_by(ScheduledTask.date)).scalars().all()
    )


@router.get("/today", response_model=list[ScheduledTaskItem])
def today(db: DatabaseSession):
    """
    Returns list of tasks scheduled for today.

    """
    start = start_of_day(datetime.now(UTC))
    end = start + timedelta(days=1)
    return (
        db.execute(
            select(ScheduledTask)
            .where(ScheduledTask.date >= start, ScheduledTask.date < end)
            .order_by(ScheduledTask.date)
        )
        .scalars()
        .all()
    )


@router.get("/overdue", response_model=list[ScheduledTaskItem])
def overdue(db: DatabaseSession):
    """
    Returns list of scheduled tasks whose date has already passed.

    """
    start = start_of_day(datetime.now(UTC))
    return (
        db.execute(
            select(ScheduledTask)
            .where(ScheduledTask.date < start)
            .order_by(ScheduledTask.date)
        )
        .scalars()
        .all()
    )


@router.put("/{task_id}", response_model=ScheduledTaskItem)
def schedule(task_id: int, request: ScheduledTaskSchedule, db: DatabaseSession):
    """
    Adds a task to the scheduled list, or updates its date if it is
    already scheduled.

    """
    get_task_or_404(task_id, db)
    scheduled_task = db.execute(
        select(ScheduledTask).where(ScheduledTask.task_id == task_id)
    ).scalar_one_or_none()
    if scheduled_task is None:
        scheduled_task = ScheduledTask(task_id=task_id, date=request.date)
        db.add(scheduled_task)
    else:
        scheduled_task.date = request.date
    db.commit()
    db.refresh(scheduled_task)
    return scheduled_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def unschedule(task_id: int, db: DatabaseSession):
    """
    Removes a task from the scheduled list.

    """
    scheduled_task = get_scheduled_task_or_404(task_id, db)
    db.delete(scheduled_task)
    db.commit()


if __name__ == "__main__":
    pass
