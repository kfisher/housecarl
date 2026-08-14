# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Automated testing for the '/api/rooms' endpoints.

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


def test_all_returns_empty_list_when_no_rooms(client):
    response = client.get('/api/rooms')

    assert response.status_code == 200
    assert response.json() == []


def test_all_returns_every_room(client):
    kitchen = create_room(client, 'Kitchen')
    bathroom = create_room(client, 'Bathroom')

    response = client.get('/api/rooms')

    assert response.status_code == 200
    assert response.json() == [kitchen, bathroom]


def test_details_returns_room_with_tasks(client):
    room = create_room(client, 'Kitchen')
    task = create_task(client, room['id'])

    response = client.get(f'/api/rooms/{room["id"]}')

    assert response.status_code == 200
    body = response.json()
    assert body['id'] == room['id']
    assert body['title'] == 'Kitchen'
    assert len(body['tasks']) == 1
    assert body['tasks'][0]['id'] == task['id']
    assert body['tasks'][0]['title'] == task['title']


def test_details_returns_404_for_unknown_room(client):
    response = client.get('/api/rooms/1')

    assert response.status_code == 404


def test_create_adds_room(client):
    response = client.post('/api/rooms', json={'title': 'Living Room'})

    assert response.status_code == 201
    body = response.json()
    assert body['title'] == 'Living Room'
    assert 'id' in body

    listed = client.get('/api/rooms').json()
    assert body in listed


def test_create_requires_title(client):
    response = client.post('/api/rooms', json={})

    assert response.status_code == 422


def test_update_changes_title(client):
    room = create_room(client, 'Kitchen')

    response = client.patch(f'/api/rooms/{room["id"]}', json={'title': 'Pantry'})

    assert response.status_code == 200
    assert response.json()['title'] == 'Pantry'

    refreshed = client.get(f'/api/rooms/{room["id"]}').json()
    assert refreshed['title'] == 'Pantry'


def test_update_without_fields_leaves_room_unchanged(client):
    room = create_room(client, 'Kitchen')

    response = client.patch(f'/api/rooms/{room["id"]}', json={})

    assert response.status_code == 200
    assert response.json()['title'] == 'Kitchen'


def test_update_returns_404_for_unknown_room(client):
    response = client.patch('/api/rooms/1', json={'title': 'Pantry'})

    assert response.status_code == 404


def test_delete_removes_room(client):
    room = create_room(client, 'Kitchen')

    response = client.delete(f'/api/rooms/{room["id"]}')

    assert response.status_code == 204
    assert client.get(f'/api/rooms/{room["id"]}').status_code == 404


def test_delete_returns_404_for_unknown_room(client):
    response = client.delete('/api/rooms/1')

    assert response.status_code == 404


def test_delete_room_cascades_to_its_tasks(client):
    room = create_room(client, 'Kitchen')
    task = create_task(client, room['id'])

    response = client.delete(f'/api/rooms/{room["id"]}')

    assert response.status_code == 204
    assert client.get(f'/api/tasks/{task["id"]}').status_code == 404


if __name__ == '__main__':
    pass

