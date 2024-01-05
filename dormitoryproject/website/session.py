from flask import session, redirect
from functools import wraps
import os
import base64


def set_session(user_id, role, remember):
    """
    Sets a new session with a random session ID, user ID, and role.

    Parameters:
        - user_id (int): The user's ID to be stored in the session.
        - role (str): The user's role to be stored in the session.
        - remember (bool): Indicates whether the session should be permanent or not.
    """
    # Generate a random session ID using 32 bytes of random data
    session_id = base64.b64encode(os.urandom(32)).decode('utf-8')

    # Update the session with user information and session ID
    session.update({'session_id': session_id, 'user_id': user_id, 'role': role})

    # Set session as permanent if 'remember' is True
    if remember:
        session.permanent = True
    else:
        session.permanent = False


def get_session():
    """
    Checks if essential session information (user ID, role, and session ID) is present.

    Returns:
        bool: True if all essential information is present, False otherwise.
    """
    if 'user_id' in session and 'role' in session and 'session_id' in session:
        return True
    else:
        return False


def delete_session():
    """
    Clears all data stored in the session.
    """
    session.clear()


def get_perm_session():
    """
    Returns the permanence status of the session.

    Returns:
        bool: True if the session is marked as permanent, False otherwise.
    """
    return session.permanent


def get_role():
    """
    Returns the user's role stored in the session.

    Returns:
        str or None: The user's role or None if not present.
    """
    return session.get('role')


def user_id():
    """
    Returns the user ID stored in the session as an integer.

    Returns:
        int or None: The user ID or None if not present.
    """
    return int(session.get('user_id'))


def logged_in(arg_list):
    """
    Decorator function to restrict access to certain views based on user roles.

    Parameters:
        - arg_list (list): List of roles allowed to access the decorated view.

    Returns:
        function: Decorated function with access control.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if the user is logged in and has the required role
            if get_session() and get_role() in arg_list:
                return f(*args, **kwargs)
            else:
                # Redirect to '404' if not logged in or role is not authorized
                return redirect('/404')
        return wrapper

    return decorator
