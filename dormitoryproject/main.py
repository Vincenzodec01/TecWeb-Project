from website import create_app
import os
from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

# Function to clean up expired sessions in the 'flask_session' folder
def cleanup_expired_sessions():
    session_folder = 'flask_session'

    # List files in the session folder
    session_files = os.listdir(session_folder)

    # Current timestamp
    current_timestamp = datetime.now().timestamp()

    for session_file in session_files:
        file_path = os.path.join(session_folder, session_file)

        # Get the last modification time of the file (timestamp)
        last_modified_timestamp = os.path.getmtime(file_path)

        # Calculate the age of the session in seconds
        session_age = current_timestamp - last_modified_timestamp

        # Maximum session age (1 year in seconds)
        max_session_age = 365 * 24 * 60 * 60

        # If the session has expired, delete the file
        if session_age > max_session_age:
            os.remove(file_path)


if __name__ == '__main__':
    # Create a background scheduler
    scheduler = BackgroundScheduler()

    # Schedule the cleanup_expired_sessions function to run every hour
    scheduler.add_job(cleanup_expired_sessions, 'interval', hours=1)

    # Start the scheduler
    scheduler.start()

    # Run the Flask app on port 5000 in debug mode
    app.run(port=5000, debug=True)
