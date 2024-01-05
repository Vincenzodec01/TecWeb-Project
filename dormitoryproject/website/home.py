from flask import Blueprint, render_template, request, redirect, url_for
from website.session import get_session, get_role
from website.database import UserDB

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    """
    Displays the home page.

    Returns:
        render_template: Renders the 'index.html' template with session status and user role.
    """
    if request.method == "POST":
        # Handle room search form submission
        checkIn = request.form.get('checkin')
        checkOut = request.form.get('checkout')
        adults = request.form.get('adults')
        return redirect(url_for('home.search_room', check_in=checkIn, check_out=checkOut, adults=adults))

    return render_template('index.html', val_session=get_session(), role=get_role())


@home.route('/contacts', methods=['GET', 'POST'])
def contacts():
    """
    Displays the contacts page and handles the contact form submission.

    Returns:
        render_template: Renders the 'contacts.html' template with session status and user role.
    """
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        print(request.form.get('genderOption'))  # Consider handling the gender option

    return render_template('contacts.html', val_session=get_session(), role=get_role())


@home.route('/search/<check_in>+<check_out>+<adults>', methods=['GET', 'POST'])
def search_room(check_in, check_out, adults):
    """
    Displays the search results for available rooms based on the specified criteria.

    Parameters:
        - check_in (str): The check-in date for the room search.
        - check_out (str): The check-out date for the room search.
        - adults (str): The number of adults for the room search.

    Returns:
        render_template: Renders the 'room/search-room.html' template with search results and session status.
    """

    rooms = UserDB.query(
        'SELECT CONVERT(t2.id_type, CHAR), CONCAT(UCASE(LEFT(t2.name_type, 1)), SUBSTRING(t2.name_type, 2)), t1.available, IF(SUBSTRING_INDEX(CONVERT(t2.price, CHAR), \'.\', -1) = \'0\', CONVERT(t2.price, SIGNED), CONVERT(t2.price, CHAR)), p2.id_promotion, p2.promotion_name, p2.p_end_date, p2.percent_discount, (t2.price - p2.percent_discount*t2.price/100) FROM (SELECT t2.id_type, (total_room - COALESCE(t1.busy_room, 0)) as available FROM (SELECT id_type, count(*) AS busy_room FROM reservation WHERE (check_in_date >= %s AND check_in_date <= %s) OR (check_out_date >= %s AND check_out_date <= %s) OR (check_in_date <= %s AND check_out_date >= %s) GROUP BY id_type) t1 right JOIN (SELECT id_type, count(*) AS total_room FROM room GROUP BY id_type) t2 ON t1.id_type = t2.id_type) t1 JOIN room_type t2 on t1.id_type=t2.id_type LEFT JOIN apply_promotion p1 on t2.id_type = p1.id_type LEFT JOIN (SELECT * FROM promotion WHERE p_start_date <= now() and p_end_date >= now()) p2 on p1.id_promotion = p2.id_promotion WHERE t2.adults = %s',
        (check_in, check_out, check_in, check_out, check_in, check_out, adults))

    print(rooms)

    return render_template('room/search-room.html', val_session=get_session(), role=get_role(), rooms=rooms,
                           check_in=check_in, check_out=check_out, adults=adults)


@home.route('/search', methods=['GET', 'POST'])
def search():
    """
    Handles the search functionality for available rooms based on user input.

    If the request method is POST, it extracts the check-in date, check-out date, and number of adults from the form
    and redirects to the 'search_room' route with the provided parameters.

    If the request method is GET, it renders the 'search-room.html' template with session status, user role, and
    placeholders for room information, check-in date, check-out date, and number of adults.

    Returns:
        render_template or redirect: Renders the template or redirects to the 'search_room' route.
    """
    if request.method == 'POST':
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        adults = request.form.get('adults')
        return redirect(url_for('home.search_room', check_in=check_in, check_out=check_out, adults=adults))

    return render_template('room/search-room.html', val_session=get_session(), role=get_role(), rooms=0, check_in=0, check_out=0, adults=0)
