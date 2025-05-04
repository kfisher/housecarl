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
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_rooms():
    """
    Tests GET /api/v1/rooms endpoint.

    """
    response = client.get('/api/v1/rooms')
    assert response.status_code == 200
    # TODO: Validate the JSON response
    # assert response.json() == ?

def test_read_room():
    """
    Tests GET /api/v1/rooms/{room_id} endpoint.

    """
    response = client.get('/api/v1/rooms/1')
    assert response.status_code == 200
    # TODO: Validate the JSON response
    # assert response.json() == ?

def test_read_room_not_found():
    """
    Tests GET /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.get('/api/v1/rooms/999')
    assert response.status_code == 404

def test_create_room():
    """
    Tests POST /api/v1/rooms endpoint.

    """
    response = client.post('/api/v1/rooms', json={'name': 'Kitchen'})
    assert response.status_code == 201
    # TODO: Validate the JSON response
    # TODO: Validate that the room was actually created
    # assert response.json() == ?

def test_create_room_invalid():
    """
    Tests POST /api/v1/rooms endpoint with invalid data.

    """
    response = client.post('/api/v1/rooms', json={'name': ''})
    assert response.status_code == 422

def test_update_room():
    """
    Tests PUT /api/v1/rooms/{room_id} endpoint.

    """
    response = client.put('/api/v1/rooms/1', json={'name': 'Updated Kitchen'})
    assert response.status_code == 200
    # TODO: Validate that the data was actually updated.

def test_update_room_not_found():
    """
    Tests PUT /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.put('/api/v1/rooms/999', json={'name': 'Updated Kitchen'})
    assert response.status_code == 404

def test_update_room_invalid():
    """
    Tests PUT /api/v1/rooms/{room_id} endpoint with invalid data.

    """
    response = client.put('/api/v1/rooms/1', json={'name': ''})
    assert response.status_code == 422

def test_delete_room():
    """
    Tests DELETE /api/v1/rooms/{room_id} endpoint.

    """
    response = client.delete('/api/v1/rooms/1')
    assert response.status_code == 204
    # TODO: Validate that the room was actually deleted

def test_delete_room_not_found():
    """
    Tests DELETE /api/v1/rooms/{room_id} endpoint with a non-existent room.

    """
    response = client.delete('/api/v1/rooms/999')
    assert response.status_code == 404

if __name__ == '__main__':
    pass
