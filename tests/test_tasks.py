# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Automated testing for the '/api/tasks' endpoints.

"""


def create_room(client, title='Kitchen'):
    """
    Creates a room via the API and returns the parsed response body.

    """
    response = client.post('/api/rooms', json={'title': title})
    assert response.status_code == 201
    return response.json()


def create_task(client, room_id, **overrides):
    """
    Creates a task via the API and returns the parsed response body.

    """
    payload = {
        'title': 'Clean counters',
        'state': 4,
        'frequency': 'P1D',
        'room_id': room_id,
    }
    payload.update(overrides)

    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    return response.json()


def test_all_returns_empty_list_when_no_tasks(client):
    response = client.get('/api/tasks')

    assert response.status_code == 200
    assert response.json() == []


def test_all_returns_every_task(client):
    room = create_room(client)
    counters = create_task(client, room['id'], title='Clean counters')
    floors = create_task(client, room['id'], title='Sweep floors')

    response = client.get('/api/tasks')

    assert response.status_code == 200
    assert response.json() == [counters, floors]


def test_details_returns_task(client):
    room = create_room(client)
    task = create_task(client, room['id'], description='Wipe down all surfaces')

    response = client.get(f'/api/tasks/{task["id"]}')

    assert response.status_code == 200
    body = response.json()
    assert body['id'] == task['id']
    assert body['title'] == 'Clean counters'
    assert body['description'] == 'Wipe down all surfaces'
    assert body['state'] == 4
    assert body['frequency'] == 'P1D'
    assert 'last_performed' in body
    assert 'last_inspected' in body


def test_details_returns_404_for_unknown_task(client):
    response = client.get('/api/tasks/1')

    assert response.status_code == 404


def test_create_adds_task(client):
    room = create_room(client)

    response = client.post(
        '/api/tasks',
        json={
            'title': 'Clean counters',
            'state': 4,
            'frequency': 'P1D',
            'room_id': room['id'],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body['title'] == 'Clean counters'
    assert body['state'] == 4
    assert 'id' in body

    listed = client.get('/api/tasks').json()
    assert body in listed


def test_create_requires_title(client):
    room = create_room(client)

    response = client.post(
        '/api/tasks',
        json={'state': 4, 'frequency': 'P1D', 'room_id': room['id']},
    )

    assert response.status_code == 422


def test_create_returns_404_for_unknown_room(client):
    response = client.post(
        '/api/tasks',
        json={
            'title': 'Clean counters',
            'state': 4,
            'frequency': 'P1D',
            'room_id': 1,
        },
    )

    assert response.status_code == 404


def test_update_changes_fields(client):
    room = create_room(client)
    task = create_task(client, room['id'])

    response = client.patch(
        f'/api/tasks/{task["id"]}',
        json={'title': 'Deep clean counters', 'description': 'Use degreaser'},
    )

    assert response.status_code == 200
    body = response.json()
    assert body['title'] == 'Deep clean counters'

    refreshed = client.get(f'/api/tasks/{task["id"]}').json()
    assert refreshed['title'] == 'Deep clean counters'
    assert refreshed['description'] == 'Use degreaser'


def test_update_changes_state(client):
    room = create_room(client)
    task = create_task(client, room['id'], state=4)

    response = client.patch(f'/api/tasks/{task["id"]}', json={'state': 2})

    assert response.status_code == 200
    assert response.json()['state'] == 2

    refreshed = client.get(f'/api/tasks/{task["id"]}').json()
    assert refreshed['state'] == 2


def test_update_without_fields_leaves_task_unchanged(client):
    room = create_room(client)
    task = create_task(client, room['id'])

    response = client.patch(f'/api/tasks/{task["id"]}', json={})

    assert response.status_code == 200
    assert response.json()['title'] == task['title']


def test_update_returns_404_for_unknown_task(client):
    response = client.patch('/api/tasks/1', json={'title': 'Deep clean counters'})

    assert response.status_code == 404


def test_update_room_id_returns_404_for_unknown_room(client):
    room = create_room(client)
    task = create_task(client, room['id'])

    response = client.patch(f'/api/tasks/{task["id"]}', json={'room_id': 999})

    assert response.status_code == 404


def test_update_can_move_task_to_another_room(client):
    room = create_room(client, 'Kitchen')
    other_room = create_room(client, 'Bathroom')
    task = create_task(client, room['id'])

    response = client.patch(
        f'/api/tasks/{task["id"]}',
        json={'room_id': other_room['id']},
    )

    assert response.status_code == 200


def test_delete_removes_task(client):
    room = create_room(client)
    task = create_task(client, room['id'])

    response = client.delete(f'/api/tasks/{task["id"]}')

    assert response.status_code == 204
    assert client.get(f'/api/tasks/{task["id"]}').status_code == 404


def test_delete_returns_404_for_unknown_task(client):
    response = client.delete('/api/tasks/1')

    assert response.status_code == 404


if __name__ == '__main__':
    pass
