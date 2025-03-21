"""
Copyright (C) 2025 Kevin Fisher

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero 
General Public License for more details.

You should have received a copy of the GNU Affero General Public License 
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from flask import Flask
from flask import Response
from flask import redirect
from flask import render_template
from flask import url_for

app = Flask(__name__)

@app.route('/')
def home() -> Response:
    """
    Redirects the base url '/' to the today page.  
    
    """
    return redirect(url_for('today'))

@app.route('/inspect')
def inspect() -> str:
    """
    Renders the Inspect page.

    """
    return render_template('inspect.html')

@app.route('/rooms/<int:room_id>')
def room(room_id: int) -> str:
    """
    Renders a Room page.

    :param room_id: 
        The unique identifier for the room.

    """
    return render_template('room.html', id=room_id)

@app.route('/today')
def today() -> str:
    """
    Renders the Today page.

    """
    return render_template('today.html')
