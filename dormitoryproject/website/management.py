import os
import shutil

import pyotp

from website.files import upload_file

from flask import Blueprint, render_template, request, flash, redirect
from website.database import UserDB
from website.session import get_session, get_role, logged_in, user_id

management = Blueprint('management', __name__)

@management.route('/manage-room')
@logged_in(['reception', 'admin'])
def manage_room():
    """
    Displays the page for managing rooms, accessible to reception and admin users.

    Returns:
        render_template: Renders the 'manage/manage-room.html' template with session status and user role.
    """
    return render_template('manage/manage-room.html', val_session=get_session(), role=get_role())

@management.route('/manage-room/number', methods=['POST', 'GET'])
@logged_in(['reception', 'admin'])
def manage_room_number():
    """
    Handles room number management, including adding, modifying, and deleting room numbers.

    Returns:
        render_template: Renders the 'manage/manage-room-number.html' template with room information.
    """
    if request.method == 'POST' and request.form.get('room-name'):
        # Handle adding new room numbers
        room_number = request.form.getlist('room-number[]')
        room_name = request.form.get('room-name')
        id_room = UserDB.query('SELECT id_type FROM room_type WHERE name_type = %s', [room_name])
        for number in room_number:
            UserDB.query('INSERT INTO room (room_number, id_type) VALUES (%s,%s)', (number, id_room[0][0]))
    elif request.method == 'POST' and request.form.get('mod-room-name'):
        # Handle modifying room numbers
        room_name = request.form.get('mod-room-name')
        room_number = request.form.get('mod-room-number')
        UserDB.call_procedure('update_room', (room_name, room_number))
    elif request.form.get('deleteRoom'):
        # Handle deleting room numbers
        room_number = str(request.form.get('deleteRoom'))
        UserDB.query('DELETE FROM room WHERE room_number=%s', [room_number])

    # Retrieve and display room information
    rooms = UserDB.query(
        'SELECT r1.room_number, r2.name_type FROM room r1 JOIN room_type r2 on r2.id_type = r1.id_type order by r1.room_number')
    return render_template('manage/manage-room-number.html', val_session=get_session(), role=get_role(), room=rooms)

@management.route('/manage-room/type', methods=['GET', 'POST'])
@logged_in(['reception', 'admin'])
def manage_room_type():
    """
    Handles room type management, including adding, modifying, and deleting room types.

    Returns:
        render_template: Renders the 'manage/manage-room_type.html' template with room type information.
    """
    if request.method == 'POST' and request.form.get('save-room') == 'insert':
        # Handle adding new room types
        room_name = request.form.get('room-name')
        room_description = request.form.get('room-description')
        room_price = request.form.get('room-price')
        optionAdults = request.form.get('optionAdults')
        UserDB.call_procedure('add_type_room', (room_name, room_description, room_price, optionAdults))
        id_type = UserDB.query('SELECT id_type FROM room_type WHERE name_type=%s', [room_name])
        id_type = id_type[0][0]
        upload_file(request.files.getlist('room-img'), 'website/static/img/img-room/id-', id_type)
    elif request.method == 'POST' and request.form.get('save-room') == 'modify':
        # Handle modifying room types
        id_room = request.form.get('mod-id-room')
        room_description = request.form.get('mod-room-description')
        room_price = request.form.get('mod-room-price')
        UserDB.query('UPDATE room_type SET description=%s, price=%s WHERE id_type=%s',
                     (room_description, room_price, id_room))
    elif request.form.get('deleteRoom'):
        # Handle deleting room types
        id_room = request.form.get('deleteRoom')
        UserDB.query('DELETE FROM room_type WHERE id_type=%s', [id_room])

    # Retrieve and display room type information
    room = UserDB.query('SELECT * FROM room_type')
    return render_template('manage/manage-room_type.html', val_session=get_session(), room=room, role=get_role())

@management.route('/clean-room', methods=['GET', 'POST'])
@logged_in(['cleaner', 'admin'])
def clean_room():
    """
    Handles the cleaning of rooms, accessible to cleaner and admin users.

    Returns:
        render_template: Renders the 'manage/clean-room.html' template with room information.
    """
    if request.method == 'POST':
        cleaned_rooms = request.form.getlist('checkRoom')
        id_staff = user_id()
        for cleaned_room in cleaned_rooms:
            UserDB.call_procedure('add_clean_room', (id_staff, cleaned_room))

    # Retrieve and display rooms that need cleaning
    room = UserDB.query('SELECT * FROM view_room_not_cleaned')
    return render_template('manage/clean-room.html', val_session=get_session(), role=get_role(), rooms=room)

@management.route('/manage-promotion', methods=['GET', 'POST'])
@logged_in(['reception', 'admin'])
def manage_promotion():
    """
    Handles promotion management, including adding, modifying, and deleting promotions.

    Returns:
        render_template: Renders the 'manage/manage-promotion.html' template with promotion information.
    """
    if request.method == 'POST' and request.form.get('deletePromotion'):
        # Handle deleting promotions
        id_promotion = request.form.get('deletePromotion')
        UserDB.call_procedure('delete_promotion', [id_promotion])
    elif request.method == 'POST':
        # Handle adding or modifying promotions
        id_promotion = request.json['promotion_id']
        name_room = request.json['room_name']
        name_promotion = request.json['promotion_name']
        start_date = request.json['promotion_start']
        end_date = request.json['promotion_end']
        discount = request.json['promotion_discount']

        if not id_promotion:
            # Handle adding new promotions
            UserDB.call_procedure('add_promotion', (name_promotion, start_date, end_date, discount))
            id_promotion = UserDB.query('SELECT * FROM promotion where promotion_name = %s', [name_promotion])[0][0]
            for room in name_room:
                UserDB.call_procedure('add_promotion_room', (id_promotion, room))
        else:
            # Handle modifying existing promotions
            UserDB.call_procedure('modify_promotion', (id_promotion, name_promotion, start_date, end_date, discount))

        return {'response': True}

    # Retrieve and display promotion information
    promotion = UserDB.query('SELECT * FROM view_promotion')
    return render_template('manage/manage-promotion.html', val_session=get_session(), role=get_role(),
                           promotions=promotion)

@management.route('/create-user', methods=['GET', 'POST'])
@logged_in(['admin'])
def create_user():
    """
    Handles the creation of user accounts, accessible to admin users only.

    Returns:
        render_template: Renders the 'manage/create-user.html' template with session status and user role.
    """
    if request.method == 'POST':
        # Handle creating a new user
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('passw')
        role = request.form.get('roleOption')
        gender = request.form.get('genderOption')
        fiscalCode = request.form.get('fiscalCode')
        phone = str(request.form.get('phone'))
        confirmPassword = request.form.get('confirmPassw')
        print(name, surname, email, password, role, gender, phone)

        if password != confirmPassword:
            flash('Password and Confirm Password must be the same', 'alert-danger')
        else:
            secret = pyotp.random_base32()
            UserDB.call_procedure('create_staff', (fiscalCode, password, name, surname, email, gender, role, phone, secret))
            staff_id = str(UserDB.query('SELECT id_staff FROM staff WHERE s_fiscal_code = %s', [fiscalCode])[0][0])
            os.mkdir('website/static/img/avatar-staff/id-' + staff_id)
            shutil.copy('website/static/img/avatar-staff/default.webp',
                        'website/static/img/avatar-staff/id-' + staff_id + '/default.webp')
            UserDB.query('INSERT INTO avatar_staff (id_avatar, name_avatar, id_user) VALUES (0, %s, %s)',
                         ('default.webp', int(staff_id)))
            flash('User successfully created', 'alert-success')

    return render_template('manage/create-user.html', val_session=get_session(), role=get_role())


@management.route('/delete_room_type/<id_room>')
def delete_room_type(id_room):
    """
    Handles the deletion of a room type. Redirects to the 'manage-room/type' page after deletion.

    Args:
        id_room (str): The id of the room type to be deleted.

    Returns:
        redirect: Redirects to the 'manage-room/type' page.
    """
    UserDB.query('DELETE FROM room_type WHERE id_type=%s', [id_room])
    print(id_room)
    return redirect('/manage-room/type')

@management.route('/delete_room_number/<id_room>')
def delete_room_number(id_room):
    """
    Handles the deletion of a room number. Redirects to the 'manage-room/number' page after deletion.

    Args:
        id_room (str): The id of the room number to be deleted.

    Returns:
        redirect: Redirects to the 'manage-room/number' page.
    """
    room_number = str(id_room)
    UserDB.query('DELETE FROM room WHERE room_number=%s', [room_number])
    return redirect('/manage-room/number')
