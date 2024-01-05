import os


import os

def upload_file(file_list, path, _id=None, file_counter=1):
    """
    Uploads files to the specified path with an optional subdirectory based on the provided ID.

    Parameters:
        - file_list (list): List of files to be uploaded.
        - path (str): Base path for file upload.
        - _id (str): Optional subdirectory ID.
        - file_counter (int): Counter for naming files.

    Returns:
        None
    """
    # Create a subdirectory with the provided ID (if provided)
    os.mkdir(path + f'{_id}')

    # Iterate through the list of files
    for file in file_list:
        # Extract file extension
        file_extension = os.path.splitext(file.filename)[1]
        # Construct a unique file name using the counter and extension
        file_name = f'{file_counter}{file_extension}'

        # Check if the file has a valid name
        if file.filename != '':
            # Save the file to the specified path
            file.save(os.path.join(path + f'{_id}', file_name))
            file_counter += 1  # Increment the counter for the next file
