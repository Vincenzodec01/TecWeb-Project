from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from website.session import *
from website.database import UserDB

payment = Blueprint('payment', __name__)


@payment.route('/checkout/review/cod=<id_room>+checkin=<check_in>+checkout=<check_out>', methods=['GET', 'POST'])
def payment_view(id_room, check_in, check_out):
    """
    Displays the payment review page for a selected room reservation, allowing users to proceed to payment.

    Parameters:
        - id_room (str): The ID of the room for which the payment is being processed.
        - check_in (str): The check-in date of the reservation.
        - check_out (str): The check-out date of the reservation.

    Returns:
        render_template: Renders the 'payment/checkout.html' template with room and payment information.
    """
    price = 0.0
    if request.method == 'POST' and request.form.get('pay'):
        # Handle payment confirmation
        return redirect(url_for('payment.payment_success', id_room=id_room, check_in=check_in, check_out=check_out))

    # Retrieve room price and name from the database
    price = round(UserDB.call_procedure('view_price', (id_room, price))[1], 2)
    name_room = UserDB.query('SELECT name_type FROM room_type WHERE id_type = %s', [id_room])[0][0]

    # Retrieve user's saved payment methods from the database
    c_card = UserDB.query('SELECT name, number_card, exp, cvc, type FROM payment_method WHERE id_user = %s',
                          [user_id()])

    return render_template('payment/checkout.html', name_room=name_room, price=price, cards=c_card,
                           val_session=get_session(), role=get_role(), id_room=id_room, check_in=check_in,
                           check_out=check_out)


@payment.route('/checkout/success+cod=<id_room>+check_in=<check_in>+check_out=<check_out>', methods=['GET', 'POST'])
def payment_success(id_room, check_in, check_out):
    """
    Displays the payment success page after completing a room reservation.

    Parameters:
        - id_room (str): The ID of the room for which the payment has been successfully processed.
        - check_in (str): The check-in date of the reservation.
        - check_out (str): The check-out date of the reservation.

    Returns:
        redirect: Redirects to the home page after successfully completing the reservation.
    """
    price = 0.0

    # Retrieve room price and name from the database
    price = round(UserDB.call_procedure('view_price', (id_room, price))[1], 2)
    name_room = UserDB.query('SELECT name_type FROM room_type WHERE id_type = %s', [id_room])[0][0]

    # Call stored procedure to add the reservation to the database
    UserDB.call_procedure('add_reservation', (check_in, check_out, user_id(), name_room, price))

    return redirect(url_for('home.index'))
