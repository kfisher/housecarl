# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Automated testing for the '/api/scheduled-tasks' endpoints.

"""

from datetime import UTC, datetime, timedelta


def create_room(client, title="Kitchen"):
    """
    Creates a room via the API and returns the parsed response body.

    """
    response = client.post("/api/rooms", json={"title": title})
    assert response.status_code == 201
    return response.json()


def create_task(client, room_id, **overrides):
    """
    Creates a task via the API and returns the parsed response body.

    """
    payload = {
        "title": "Clean counters",
        "state": 3,
        "frequency": "P1D",
        "room_id": room_id,
    }
    payload.update(overrides)

    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def schedule_task(client, task_id, date):
    """
    Schedules a task via the API and returns the parsed response body.

    """
    response = client.put(
        f"/api/scheduled-tasks/{task_id}",
        json={"date": date.isoformat()},
    )
    assert response.status_code == 200
    return response.json()


def test_all_returns_empty_list_when_no_scheduled_tasks(client):
    response = client.get("/api/scheduled-tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_schedule_adds_task(client):
    room = create_room(client)
    task = create_task(client, room["id"])
    date = datetime.now(UTC)

    body = schedule_task(client, task["id"], date)

    assert body["task"]["id"] == task["id"]
    assert "id" in body

    listed = client.get("/api/scheduled-tasks").json()
    assert body in listed


def test_schedule_returns_404_for_unknown_task(client):
    response = client.put(
        "/api/scheduled-tasks/1",
        json={"date": datetime.now(UTC).isoformat()},
    )

    assert response.status_code == 404


def test_schedule_updates_existing_entry_instead_of_duplicating(client):
    room = create_room(client)
    task = create_task(client, room["id"])
    first_date = datetime.now(UTC)
    second_date = first_date + timedelta(days=3)

    first = schedule_task(client, task["id"], first_date)
    second = schedule_task(client, task["id"], second_date)

    assert first["id"] == second["id"]

    listed = client.get("/api/scheduled-tasks").json()
    assert len(listed) == 1
    assert listed[0]["date"] == second["date"]


def test_unschedule_removes_task(client):
    room = create_room(client)
    task = create_task(client, room["id"])
    schedule_task(client, task["id"], datetime.now(UTC))

    response = client.delete(f"/api/scheduled-tasks/{task['id']}")

    assert response.status_code == 204
    assert client.get("/api/scheduled-tasks").json() == []


def test_unschedule_returns_404_for_task_not_scheduled(client):
    room = create_room(client)
    task = create_task(client, room["id"])

    response = client.delete(f"/api/scheduled-tasks/{task['id']}")

    assert response.status_code == 404


def test_unschedule_returns_404_for_unknown_task(client):
    response = client.delete("/api/scheduled-tasks/1")

    assert response.status_code == 404


def test_today_returns_only_tasks_scheduled_for_today(client):
    room = create_room(client)
    today_task = create_task(client, room["id"], title="Today task")
    future_task = create_task(client, room["id"], title="Future task")
    past_task = create_task(client, room["id"], title="Past task")

    schedule_task(client, today_task["id"], datetime.now(UTC))
    schedule_task(client, future_task["id"], datetime.now(UTC) + timedelta(days=2))
    schedule_task(client, past_task["id"], datetime.now(UTC) - timedelta(days=2))

    response = client.get("/api/scheduled-tasks/today")

    assert response.status_code == 200
    body = response.json()
    assert [entry["task"]["title"] for entry in body] == ["Today task"]


def test_overdue_returns_only_tasks_scheduled_before_today(client):
    room = create_room(client)
    today_task = create_task(client, room["id"], title="Today task")
    future_task = create_task(client, room["id"], title="Future task")
    past_task = create_task(client, room["id"], title="Past task")

    schedule_task(client, today_task["id"], datetime.now(UTC))
    schedule_task(client, future_task["id"], datetime.now(UTC) + timedelta(days=2))
    schedule_task(client, past_task["id"], datetime.now(UTC) - timedelta(days=2))

    response = client.get("/api/scheduled-tasks/overdue")

    assert response.status_code == 200
    body = response.json()
    assert [entry["task"]["title"] for entry in body] == ["Past task"]


if __name__ == "__main__":
    pass
