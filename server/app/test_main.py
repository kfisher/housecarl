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
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from .main import app
from .db import Room, get_session

@pytest.fixture(name='session')
def session_fixture():
    """
    Fixture to create a test database session.

    """
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name='client')
def client_fixture(session):
    """
    Fixture to create a test client.

    """
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_read_rooms(session: Session, client: TestClient):
    """
    Tests GET /api/v1/rooms endpoint.

    """
    room_0 = Room(name='Living Room')
    room_1 = Room(name='Kitchen')
    session.add(room_0)
    session.add(room_1)
    session.commit()

    response = client.get('/api/v1/rooms')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]['name'] == 'Living Room'
    assert data[1]['name'] == 'Kitchen'

def test_read_room(session: Session, client: TestClient):
    """
    Tests GET /api/v1/rooms/{room_id} endpoint.

    """
    room_0 = Room(name='Bedroom')
    session.add(room_0)
    session.commit()

    response = client.get(f'/api/v1/rooms/{room_0.id}')
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == 'Bedroom'


def test_read_room_not_found(client: TestClient):
    """
    Tests GET /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.get('/api/v1/rooms/999')
    assert response.status_code == 404

def test_create_room(session: Session, client: TestClient):
    """
    Tests POST /api/v1/rooms endpoint.

    """
    response = client.post('/api/v1/rooms', json={'name': 'Laundry Room'})
    data = response.json()
    room_in_db = session.get(Room, data['id'])

    assert response.status_code == 201
    assert room_in_db is not None
    assert room_in_db.name == 'Laundry Room'
    assert data['name'] == 'Laundry Room'

def test_create_room_invalid(client: TestClient):
    """
    Tests POST /api/v1/rooms endpoint with invalid data.

    """
    response = client.post('/api/v1/rooms', json={})
    assert response.status_code == 422

def test_create_room_empty_name(client: TestClient):
    """
    Tests POST /api/v1/rooms endpoint with an empty name.

    """
    response = client.post('/api/v1/rooms', json={'name': ''})
    assert response.status_code == 422

# TODO: Test for unique constraint violation - creation.

def test_update_room(session: Session, client: TestClient):
    """
    Tests PATCH /api/v1/rooms/{room_id} endpoint.

    """
    room_0 = Room(name='Drawing')
    session.add(room_0)
    session.commit()

    response = client.patch(
        f'/api/v1/rooms/{room_0.id}',
        json={'name': 'Study'}
    )
    room_in_db = session.get(Room, room_0.id)

    assert response.status_code == 204
    assert room_in_db.name == 'Study'

def test_update_room_not_found(client: TestClient):
    """
    Tests PATCH /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.patch(
        '/api/v1/rooms/999', 
        json={'name': 'Updated Kitchen'}
    )
    assert response.status_code == 404

def test_update_room_no_name_change(session: Session, client: TestClient):
    """
    Tests PATCH /api/v1/rooms/{room_id} endpoint where the request does
    not change the name.

    """
    room_0 = Room(name='Drawing')
    session.add(room_0)
    session.commit()

    response = client.patch(f'/api/v1/rooms/{room_0.id}', json={})
    room_in_db = session.get(Room, room_0.id)

    assert response.status_code == 204
    assert room_in_db.name == 'Drawing'

def test_update_room_empty_name(session: Session, client: TestClient):
    """
    Tests PATCH /api/v1/rooms/{room_id} endpoint with an empty name.

    """
    room_0 = Room(name='Drawing')
    session.add(room_0)
    session.commit()

    response = client.patch(f'/api/v1/rooms/{room_0.id}', json={'name': ''})

    assert response.status_code == 422

# TODO: Test for unique constraint violation - update.

def test_delete_room(session: Session, client: TestClient):
    """
    Tests DELETE /api/v1/rooms/{room_id} endpoint.

    """
    room_0 = Room(name='Bathroom')
    session.add(room_0)
    session.commit()

    response = client.delete(f'/api/v1/rooms/{room_0.id}')
    room_in_db = session.get(Room, room_0.id)

    assert response.status_code == 204
    assert room_in_db is None

def test_delete_room_not_found(client: TestClient):
    """
    Tests DELETE /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.delete('/api/v1/rooms/999')
    assert response.status_code == 404

if __name__ == '__main__':
    pass
