import mysql.connector


# If something went wrong (exception)
def mysql_error(err):
    """
    Prints an error message for MySQL-related errors.

    Parameters:
        - err (mysql.connector.Error): The MySQL connector error object.

    Returns:
        None
    """
    print("Something went wrong: {}".format(err))


class DataBase:
    def __init__(self, user, password):
        """
        Initializes a database connection with the provided user and password.

        Parameters:
            - user (str): MySQL database user.
            - password (str): Password for the specified user.
        """
        self.cnx = None
        self.cursor = None
        self.config = {'user': user,
                       'password': password,
                       'host': '127.0.0.1',
                       'database': 'dormitory',
                       'raise_on_warnings': True}

    def connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            None
        """
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def close(self):
        """
        Closes the database connection and cursor.

        Returns:
            None
        """
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        """
        Commits the changes to the database.

        Returns:
            None
        """
        self.cnx.commit()

    def rollback(self):
        """
        Rolls back changes in case of an error.

        Returns:
            None
        """
        self.cnx.rollback()

    def call_procedure(self, procedure, args=()):
        """
        Calls a stored procedure with the provided arguments.

        Parameters:
            - procedure (str): The name of the stored procedure.
            - args (tuple): Arguments to be passed to the stored procedure.

        Returns:
            result: The result of the stored procedure execution.
        """
        self.connect()
        try:
            result = self.cursor.callproc(procedure, args)
            self.commit()
            return result
        except mysql.connector.Error as err:
            self.rollback()
            mysql_error(err)
            return None
        finally:
            self.close()

    def query(self, query, args=()):
        """
        Executes a SQL query with the provided arguments.

        Parameters:
            - query (str): The SQL query to be executed.
            - args (tuple): Arguments to be passed to the query.

        Returns:
            result: The result of the SQL query execution.
        """
        self.connect()
        try:
            _query = (query)
            self.cursor.execute(_query, args)
            result = self.cursor.fetchall()
            self.commit()
            return result
        except mysql.connector.Error as err:
            self.rollback()
            mysql_error(err)
            return None
        finally:
            self.close()


# Initialize instances for different user roles
UserDB = DataBase('admin', 'admin')  # User database instance
AdminDB = DataBase('admin', 'admin')  # Admin database instance
ReceptionDB = DataBase('reception', 'reception')  # Reception database instance
CleanerDB = DataBase('cleaner', 'cleaner')  # Cleaner database instance

