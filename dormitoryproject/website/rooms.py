from flask import Blueprint, render_template, request, redirect, url_for
from website.database import UserDB
from website.session import get_session, get_role

rooms = Blueprint('rooms', __name__)


@rooms.route('/rooms', methods=['GET', 'POST'])
def rooms_list():
    """
    Displays a list of rooms. Handles both GET and POST requests.
    If a POST request is made, redirects to the detailed view of the selected room.

    Returns:
        render_template: Renders the 'room/rooms.html' template with room information.
    """
    if request.method == 'POST':
        room = UserDB.query('SELECT id_type, name_type FROM room_type')
        for room_name in room:
            if int(request.form.get('sub_button')) == room_name[0]:
                return redirect(url_for('rooms.rooms_view', id_type=room_name[0]))

    # Retrieve room information from the database
    room = UserDB.query(
        'SELECT CONVERT(id_type, CHAR), CONCAT(UCASE(LEFT(name_type, 1)), SUBSTRING(name_type, 2)), CONVERT(price, DECIMAL(10,0) ), description FROM room_type')

    # Render the template with room information, session status, and user role
    return render_template('room/rooms.html', room=room, val_session=get_session(), role=get_role())


@rooms.route('/rooms/view/cod-room=<id_type>', methods=['GET', 'POST'])
def rooms_view(id_type):
    """
    Displays detailed information about a specific room.

    Parameters:
        id_type (str): The ID of the room to be displayed.

    Returns:
        render_template: Renders the 'room/rooms-detail.html' template with room details.
    """
    # Retrieve detailed information about the specified room from the database
    room = UserDB.query('SELECT CONVERT(id_type, CHAR), CONCAT(UCASE(LEFT(name_type, 1)), SUBSTRING(name_type, 2)), CONVERT(price, DECIMAL(10,0)), description, adults FROM room_type WHERE id_type=%s', [id_type])

    # Render the template with room details, session status, and user role
    return render_template('room/rooms-detail.html', _room_=room[0], val_session=get_session(), role=get_role())
