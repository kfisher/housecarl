# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Automated testing for the '/api/random-tasks' endpoints.

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


def make_overdue_task(client, room_id, **overrides):
    """
    Creates a task that is eligible for selection due to being overdue.

    The task is created with a state of Good, but with a last performed
    timestamp that exceeds its frequency.

    """
    task = create_task(client, room_id, state=3, frequency="P1D", **overrides)
    overdue = datetime.now(UTC) - timedelta(days=2)
    response = client.patch(
        f"/api/tasks/{task['id']}",
        json={"last_performed": overdue.isoformat()},
    )
    assert response.status_code == 200
    return response.json()


def make_ineligible_task(client, room_id, **overrides):
    """
    Creates a task that is not eligible for selection.

    The task is created with a state of Good and a last performed
    timestamp that does not exceed its frequency.

    """
    return create_task(client, room_id, state=3, frequency="P365D", **overrides)


def test_all_returns_empty_list_when_no_random_tasks(client):
    response = client.get("/api/random-tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_all_returns_random_tasks_sorted_by_number(client):
    room = create_room(client)
    for index in range(4):
        make_overdue_task(client, room["id"], title=f"Task {index}")

    response = client.post("/api/random-tasks", json={"count": 4})
    assert response.status_code == 201

    response = client.get("/api/random-tasks")

    assert response.status_code == 200
    body = response.json()
    assert [entry["number"] for entry in body] == sorted(
        entry["number"] for entry in body
    )


def test_generate_rejects_invalid_count(client):
    response = client.post("/api/random-tasks", json={"count": 5})

    assert response.status_code == 422


def test_generate_returns_created_status(client):
    room = create_room(client)
    make_overdue_task(client, room["id"])

    response = client.post("/api/random-tasks", json={"count": 4})

    assert response.status_code == 201


def test_generate_only_selects_eligible_tasks(client):
    room = create_room(client)
    eligible = make_overdue_task(client, room["id"], title="Overdue task")
    make_ineligible_task(client, room["id"], title="Up to date task")

    response = client.post("/api/random-tasks", json={"count": 4})

    assert response.status_code == 201
    body = response.json()
    assert len(body) == 1
    assert body[0]["task"]["title"] == eligible["title"]


def test_generate_considers_non_good_state_eligible(client):
    room = create_room(client)
    task = create_task(
        client,
        room["id"],
        title="Needs attention",
        state=1,
        frequency="P365D",
    )

    response = client.post("/api/random-tasks", json={"count": 4})

    assert response.status_code == 201
    body = response.json()
    assert len(body) == 1
    assert body[0]["task"]["title"] == task["title"]


def test_generate_caps_selection_to_available_eligible_tasks(client):
    room = create_room(client)
    make_overdue_task(client, room["id"], title="Only overdue task")

    response = client.post("/api/random-tasks", json={"count": 20})

    assert response.status_code == 201
    assert len(response.json()) == 1


def test_generate_selects_requested_count_when_enough_eligible(client):
    room = create_room(client)
    for index in range(6):
        make_overdue_task(client, room["id"], title=f"Task {index}")

    response = client.post("/api/random-tasks", json={"count": 4})

    assert response.status_code == 201
    assert len(response.json()) == 4


def test_generate_replaces_existing_random_tasks(client):
    room = create_room(client)
    for index in range(4):
        make_overdue_task(client, room["id"], title=f"First round {index}")

    first = client.post("/api/random-tasks", json={"count": 4})
    assert first.status_code == 201

    # More eligible tasks now exist than before, so a second generation
    # draws from a larger pool. If the old entries were not cleared, the
    # list would grow to more than the newly requested count.
    for index in range(4):
        make_overdue_task(client, room["id"], title=f"Second round {index}")

    second = client.post("/api/random-tasks", json={"count": 4})
    assert second.status_code == 201

    listed = client.get("/api/random-tasks").json()
    assert len(listed) == 4
    assert [entry["id"] for entry in listed] == [entry["id"] for entry in second.json()]


if __name__ == "__main__":
    pass
