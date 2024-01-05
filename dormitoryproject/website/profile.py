import requests
from flask import Blueprint, render_template, request, redirect
from website.session import *
from website.database import UserDB

profile = Blueprint('profile', __name__)


@profile.route('/staff-profile', methods=['GET', 'POST'])
@logged_in(['reception', 'admin', 'cleaner'])
def staff_profile():
    """
    Route for displaying and updating the profile of staff members.

    Returns:
        Flask render_template: Rendered HTML template with staff profile information.
    """
    if request.method == 'POST':
        # Handle avatar upload
        avatar = request.files['avatar']
        filename = avatar.filename
        avatar.save(os.path.join('website/static/img/avatar-staff/id-' + str(user_id()), filename))
        UserDB.query('INSERT INTO avatar_staff (id_avatar, name_avatar, id_user) VALUES (0, %s, %s)', (avatar.filename, user_id()))

    # Retrieve user information and avatar details from the database
    staff = UserDB.query('SELECT s_name, s_surname, s_email, s_fiscal_code, phone, role, s_gender FROM staff WHERE id_staff = %s', [user_id()])
    name_avatar = UserDB.query('SELECT name_avatar FROM avatar_staff WHERE id_user=%s ORDER BY id_avatar desc', [user_id()])
    path_avatar = 'img/avatar-staff/id-' + str(user_id()) + '/' + name_avatar[0][0]

    return render_template('profile-staff.html', val_session=get_session(), role=get_role(), staff=staff[0], path_avatar=path_avatar)

@profile.route('/profile', methods=['GET', 'POST'])
@logged_in(['user'])
def user_profile():
    """
    Route for displaying and updating the profile of regular users.

    Returns:
        Flask render_template: Rendered HTML template with user profile information.
    """
    if request.method == 'POST':
        # Handle avatar upload
        avatar = request.files['avatar']
        filename = avatar.filename
        avatar.save(os.path.join('website/static/img/avatar/id-' + str(user_id()), filename))
        UserDB.query('INSERT INTO avatar_user (id_avatar, name_avatar, id_user) VALUES (0, %s, %s)', (avatar.filename, user_id()))

    # Retrieve user information and avatar details from the database
    user = UserDB.query(
        'SELECT matriculation_number, email, fiscal_code, name, surname, gender FROM user WHERE id_user=%s',
        [user_id()])
    name_avatar = UserDB.query('SELECT name_avatar FROM avatar_user WHERE id_user=%s ORDER BY id_avatar desc', [user_id()])
    print(name_avatar)
    path_avatar = 'img/avatar/id-' + str(user_id()) + '/' + name_avatar[0][0]

    return render_template('profile-user.html', val_session=get_session(), role=get_role(), user=user[0], path_avatar=path_avatar)


@profile.route('/mysettings', methods=['GET', 'POST'])
@logged_in(['user'])
def mysettings():
    """
    Route for displaying and updating user settings, including payment methods.

    Returns:
        Flask render_template: Rendered HTML template with user settings and payment methods.
    """
    if request.method == 'POST' and request.form.get('sub_method') == 'Aggiungi':
        # Handle adding a new payment method
        cc_name = request.form.get('cc-name')
        cc_number = request.form.get('cc-number')
        cc_exp = request.form.get('cc-exp')
        cc_cvc = request.form.get('cc-cvc')
        cc_type = 'visa'
        UserDB.query(
            'INSERT INTO payment_method (number_card, id_user, exp, name, cvc, type) VALUES (%s, %s, %s, %s, %s, %s)',
            (cc_number, user_id(), cc_exp, cc_name, cc_cvc, cc_type))
    elif request.form.get('cc-number-del'):
        # Handle deleting a payment method
        UserDB.query('DELETE FROM payment_method WHERE number_card = %s', [request.form.get('cc-number-del')])

    # Retrieve user's payment methods from the database
    card = UserDB.query('SELECT number_card, exp, name, type FROM payment_method WHERE id_user=%s', [user_id()])

    return render_template('settings/settings-user.html', val_session=get_session(), role=get_role(), cards=card)


@profile.route('/history-reservation')
@logged_in(['user'])
def history_reservation():
    """
    Route for displaying the reservation history of a user.

    Returns:
        Flask render_template: Rendered HTML template with user reservation history.
    """
    reservation = UserDB.query(
        'SELECT r1.id_reservation, r1.reservation_date, r1.check_in_date, r1.check_out_date, rt.name_type, p.total, r1.cancelled FROM reservation r1 left JOIN payment p on r1.id_reservation = p.id_reservation JOIN reservation_user r2 on r1.id_reservation = r2.id_reservation JOIN room_type rt on r1.id_type = rt.id_type WHERE r2.id_user = %s',
        [user_id()])

    return render_template('history/history-reserv.html', val_session=get_session(), role=get_role(), reservations=reservation)

@profile.route('/mypayments', methods=['GET', 'POST'])
def mypayments():
    """
    Route for displaying the payment history of a user.

    Returns:
        Flask render_template: Rendered HTML template with user payment history.
    """
    payments = UserDB.query('SELECT p.receipt_number, p.payment_date, p.total FROM payment p JOIN reservation_user r on p.id_reservation = r.id_reservation WHERE r.id_user = %s', [user_id()])
    return render_template('history/history-payment.html', val_session=get_session(), role=get_role(), payments=payments)


@profile.route('/staff-settings', methods=['GET', 'POST'])
def staff_settings():
    """
    Route for displaying and updating the settings of staff members.

    Returns:
        Flask render_template: Rendered HTML template with staff settings.
    """
    if request.method == 'POST':
        name = None if not request.form.get('name') else request.form.get('name')
        surname = None if not request.form.get('surname') else request.form.get('surname')
        email = None if not request.form.get('email') else request.form.get('email')
        phone = None if not request.form.get('phone') else request.form.get('phone')
        UserDB.query('UPDATE staff SET s_name = IF(%s is null, s_name, %s), s_surname = IF(%s is null, s_surname, %s), s_email = IF(%s is null, s_email, %s), phone = IF(%s is null, phone, %s) WHERE id_staff = %s', (name, name, surname, surname, email, email, phone, phone, user_id()))
    return render_template('settings/settings-staff.html', val_session=get_session(), role=get_role())
