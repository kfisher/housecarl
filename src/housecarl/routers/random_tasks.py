# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the random tasks endpoint.

"""

import random
from datetime import UTC, datetime

from fastapi import APIRouter, status
from sqlalchemy import delete, select

from housecarl.db import DatabaseSession
from housecarl.db.models import InspectionState, RandomTask, Task
from housecarl.schema import RandomTaskGenerate, RandomTaskItem

router = APIRouter()


def is_eligible(task: Task, now: datetime) -> bool:
    """
    Returns whether a task is eligible for random selection.

    A task is eligible if its state is not Good, or if the time since
    it was last performed exceeds its frequency.

    """
    last_performed = task.last_performed
    if last_performed.tzinfo is None:
        last_performed = last_performed.replace(tzinfo=UTC)
    return task.state != InspectionState.Good or now - last_performed > task.frequency


@router.get("", response_model=list[RandomTaskItem])
def all(db: DatabaseSession):
    """
    Returns list of all random tasks, sorted by number.

    """
    return db.execute(select(RandomTask).order_by(RandomTask.number)).scalars().all()


@router.post(
    "", response_model=list[RandomTaskItem], status_code=status.HTTP_201_CREATED
)
def generate(request: RandomTaskGenerate, db: DatabaseSession):
    """
    Generates a new set of random tasks.

    All existing random task entries are removed and replaced with a
    new random selection. Only tasks whose state is not Good, or whose
    time since last performed exceeds their frequency, are considered.

    """
    db.execute(delete(RandomTask))

    now = datetime.now(UTC)
    candidates = [
        task
        for task in db.execute(select(Task)).scalars().all()
        if is_eligible(task, now)
    ]

    selected = random.sample(candidates, k=min(request.count, len(candidates)))

    random_tasks = [
        RandomTask(number=number, task_id=task.id)
        for number, task in enumerate(selected, start=1)
    ]
    db.add_all(random_tasks)
    db.commit()
    for random_task in random_tasks:
        db.refresh(random_task)
    return random_tasks


if __name__ == "__main__":
    pass
