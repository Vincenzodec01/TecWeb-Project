from flask import Blueprint, render_template, request, url_for
import requests
from website.database import UserDB
from website.session import *
import pyotp
from io import BytesIO
import qrcode
from base64 import b64encode
import shutil

# Define a new blueprint for authentication routes
auth = Blueprint('auth', __name__)


def get_b64encoded_qr_image(data):
    """
    Generates a base64-encoded QR code image.

    Parameters:
        - data (str): Data to be encoded in the QR code.

    Returns:
        str: Base64-encoded representation of the QR code image.
    """
    print(data)
    qr = qrcode.main.QRCode(version=1, box_size=10, border=5)  # Create a QR code instance with specified settings
    qr.add_data(data)  # Add data to the QR code
    qr.make(fit=True)  # Generate the QR code
    img = qr.make_image(fill_color='black', back_color='white')  # Create an image from the QR code
    buffered = BytesIO()  # Create a buffered object to store image data
    img.save(buffered)  # Save the image to the buffer
    return b64encode(buffered.getvalue()).decode("utf-8")  # Return base64-encoded image data as a string


@auth.route('/verify2FA/<fiscal_code>&remember=<remember>', methods=['GET', 'POST'])
def verify2fa(fiscal_code, remember):
    """
    Handles the verification of two-factor authentication.

    Parameters:
        - fiscal_code (str): Fiscal code of the user.
        - remember (str): Remember flag indicating whether to persist the session.

    Returns:
        Flask redirect or render_template: Redirects to the home page or renders the 2FA verification page.
    """
    _2fa = UserDB.query('SELECT secret_key FROM staff WHERE s_fiscal_code = %s',
                        [fiscal_code])  # Fetch user's secret key
    secret_key = _2fa[0][0]  # Extract the secret key
    totp = pyotp.totp.TOTP(secret_key)  # Create a TOTP instance using the secret key

    if request.method == "POST":
        otp = request.form.get('otp1') + request.form.get('otp2') + request.form.get('otp3') + request.form.get('otp4') + request.form.get('otp5') + request.form.get('otp6')  # Get the OTP entered by the user
        print(totp.now())  # Print the current OTP (for debugging purposes)
        if totp.now() == otp:  # Check if entered OTP is valid
            staff = UserDB.query('SELECT id_staff, role FROM staff WHERE s_fiscal_code = %s',
                                 [fiscal_code])  # Fetch user's details
            set_session(staff[0][0], staff[0][1], remember)  # Set the user's session
            return redirect('/')  # Redirect to the home page
        else:
            return redirect(url_for('auth.verify2fa', fiscal_code=fiscal_code,
                                    remember=remember))  # Redirect to 2FA verification page if OTP is invalid
    return render_template('authentication/verify2fa.html', fiscal_code=fiscal_code, remember=remember)  # Render 2FA verification page


@auth.route('/setup2FA/<fiscal_code>&remember=<remember>', methods=['GET', 'POST'])
def setup2fa(fiscal_code, remember):
    """
    Handles the setup of two-factor authentication.

    Parameters:
        - fiscal_code (str): Fiscal code of the user.
        - remember (str): Remember flag indicating whether to persist the session.

    Returns:
        Flask redirect or render_template: Redirects to the 2FA setup verification page or renders the 2FA setup page.
    """
    _2fa = UserDB.query('SELECT secret_key, access FROM staff WHERE s_fiscal_code = %s',
                        [fiscal_code])  # Fetch user's secret key and access flag
    secret_key = _2fa[0][0]  # Extract the secret key
    uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=fiscal_code)  # Generate provisioning URI for TOTP

    if request.method == "POST":
        return redirect(url_for('auth.verify2fa', uri=uri, fiscal_code=fiscal_code,
                                remember=remember))  # Redirect to 2FA verification page
    base64_qr_image = get_b64encoded_qr_image(uri)  # Get base64-encoded QR code image
    return render_template('authentication/setup2fa.html', uri=uri, qr_image=base64_qr_image, fiscal_code=fiscal_code,
                           remember=remember, secret=secret_key)  # Render 2FA setup page


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login process.

    Returns:
        Flask render_template or redirect: Renders the login page or redirects to the home page.
    """
    # Initialize a message variable
    msg = None

    if get_session():
        return redirect('/')

    # If request method is POST and the user is not logged in get the data from the form
    if request.method == 'POST' and not get_session():
        print('POST LOGIN')
        fiscal_code = request.form.get('cod_fisc')
        password = request.form.get('password')
        remember = request.form.get('remember')  # Check if the "Remember Me" option is selected

        if remember:
            remember = True
        else:
            remember = False

        staff = UserDB.call_procedure('check_staff', (fiscal_code, password, 0))
        # If the procedure doesn't return any error or exception check if the flag is true
        if staff:
            staff_exist = staff[2]

            if staff_exist:
                # If exist he can login after the 2fa procedure
                return redirect(url_for('auth.setup2fa', fiscal_code=fiscal_code, remember=remember))

        # Check the student into the database
        user = UserDB.call_procedure('check_user', (fiscal_code, password, 0))
        print(user)

        # If the student exist, set session variable and redirect to homepage
        if user:
            user_exist = user[2]
            if user_exist:
                info = UserDB.query('SELECT id_user, role FROM user WHERE fiscal_code=%s', [fiscal_code])
                print(info)
                set_session(info[0][0], info[0][1], remember)
                return redirect('/')
            else:
                # If student doesn't exist, check credentials with UniParthenope API
                response = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login',
                                        auth=(fiscal_code, password))
                print(True)
                # If GET request return 200, store user into database and then redirect to homepage
                if response.status_code == 200:

                    res = response.json()
                    matr = res['user']['trattiCarriera'][0]['matricola']
                    name = res['user']['firstName']
                    surname = res['user']['lastName']
                    gender = res['user']['sex']
                    role = 'user'

                    # Method register_user calls a stored procedure which register a record into the database
                    success_create = UserDB.call_procedure('create_user', (
                        matr, None, fiscal_code, password, name, surname, gender, role))
                    if success_create is None:
                        return render_template('authentication/login.html', msg='Errore durante la creazione',
                                               val_session=get_session())
                    else:
                        user_id = UserDB.query('SELECT id_user FROM user WHERE fiscal_code=%s', [fiscal_code])[0][0]
                        set_session(user_id, role, remember)
                        user_id = str(user_id)
                        
                        os.mkdir('website/static/img/avatar/id-' + user_id)
                        shutil.copy('website/static/img/avatar/default.webp',
                                    'website/static/img/avatar/id-' + user_id + '/default.webp')
                        UserDB.query('INSERT INTO avatar_user (id_avatar, name_avatar, id_user) VALUES (0, %s, %s)',
                                     ('default.webp', int(user_id)))
                        return redirect('/')

                else:
                    # After insert wrong credentials it will print an error message
                    msg = 'Credenziali invalide'
                    return render_template('authentication/login.html', msg=msg, val_session=get_session())

    return render_template('authentication/login.html', msg=msg, val_session=get_session())


# Route for logout
@auth.route('/logout')
def logout():
    delete_session()
    return redirect('/login')
