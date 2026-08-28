# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Application entry point.

"""

from fastapi import FastAPI

from housecarl import db
from housecarl.routers import random_tasks, rooms, scheduled_tasks, tasks

db.initialize()

app = FastAPI()

app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(
    random_tasks.router,
    prefix="/api/random-tasks",
    tags=["random-tasks"],
)
app.include_router(
    scheduled_tasks.router,
    prefix="/api/scheduled-tasks",
    tags=["scheduled-tasks"],
)
