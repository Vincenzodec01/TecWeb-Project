from flask import Flask, render_template, make_response, send_from_directory
from flask_cors import CORS
import secrets
from datetime import timedelta
from flask_session import Session
from werkzeug.exceptions import HTTPException

from website.session import delete_session, get_session, get_perm_session, set_session, get_role
from flask_socketio import SocketIO
import uuid


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)  # Create a Flask application instance
    app.config["SESSION_TYPE"] = "filesystem"  # Set session type to filesystem
    app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random secret key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # Set session lifetime to 365 days
    app.config['SESSION_FILE_THRESHOLD'] = 100000000000  # Set session file threshold
    Session(app)  # Configure the Flask-Session extension
    CORS(app)  # Enable CORS for all routes

    @app.route('/mainfest.json')
    def get_mainfest():
        """
        Endpoint to retrieve the manifest.json file.

        Returns:
            Flask send_from_directory: The manifest.json file.
        """
        return send_from_directory('static', 'mainfest.json')

    @app.route('/sw.js')
    def sw():
        """
        Endpoint to retrieve the service worker script.

        Returns:
            Flask make_response: The service worker script with appropriate headers.
        """
        response = make_response(send_from_directory('static', filename='sw.js'))
        response.headers['Content-Type'] = 'application/javascript'
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/error404.html', val_session=get_session(), role=get_role()), 404

    """  
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/error500.html', val_session=get_session(), role=get_role())
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors
        if isinstance(e, HTTPException):
            return e

        # now you're handling non-HTTP exceptions only
        return render_template("error/error500.html", e=e), 500

    """
    # Import and register blueprints for different components of the application
    from .home import home
    from .auth import auth
    from .rooms import rooms
    from .profile import profile
    from .management import management
    from .payment import payment

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(rooms)
    app.register_blueprint(profile)
    app.register_blueprint(management)
    app.register_blueprint(payment)
    app.register_error_handler(404, page_not_found)
    # app.register_error_handler(500, internal_server_error)

    return app  # Return the configured Flask application
