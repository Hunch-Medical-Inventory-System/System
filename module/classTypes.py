"""
Database Management Module
--------------------------
Handles:
- Database connections
- User management
- Inventory management
- Logging

Uses MySQL with mysql-connector-python
"""

import mysql.connector
import uuid
import json
from datetime import date, datetime


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def parseJSON(filename):
    """
    Reads a JSON file and returns parsed data.

    Args:
        filename (str): Path to JSON file

    Returns:
        dict | None
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print("Error: Malformed JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

class dbConnection:
    """
    Handles MySQL database connections and transactions.
    """

    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.db = None

    def initiate(self):
        """
        Opens a connection to the MySQL database.

        Returns:
            bool
        """
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=int(self.port)
            )

            if self.db.is_connected():
                print("Successfully connected to MySQL database on port 3306!")
                return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        return False

    def cursor(self):
        """Returns a new database cursor."""
        return self.db.cursor()

    def commit(self):
        """Commits current transaction."""
        self.db.commit()

    def close(self):
        """Closes the database connection."""
        if self.db and self.db.is_connected():
            self.db.close()


# --------------------------------------------------
# Inventory Management
# --------------------------------------------------

class invManage:
    """
    Handles inventory insertions, removals, and retrieval.
    """

    def __init__(self, connection):
        self.connection = connection

    def invEntry(self, userid, upid, location, quantity, expiration, name):
        """
        Adds inventory to the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT quantity FROM inventory "
                "WHERE location = %s AND upid = %s AND expiration = %s",
                (location, upid, expiration)
            )

            result = cursor.fetchone()
            cursor.close()

            if not result:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO inventory (upid, location, quantity, expiration, name) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (upid, location, quantity, expiration, name)
                )
                self.connection.commit()
                cursor.close()
            else:
                cursor = self.connection.cursor()
                cursor.execute(
                    "UPDATE inventory SET quantity = quantity + %s "
                    "WHERE location = %s AND upid = %s AND expiration = %s",
                    (quantity, location, upid, expiration)
                )
                self.connection.commit()
                cursor.close()

            logManage(self.connection).logEntry(
                userid,
                location,
                f"Added {quantity} of {upid}"
            )

    def invRemove(self, userid, upid, location, quantity, expiration):
        """
        Removes or reduces inventory quantity.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT quantity FROM inventory "
                "WHERE location = %s AND upid = %s AND expiration = %s",
                (location, upid, expiration)
            )

            result = cursor.fetchone()
            cursor.close()

            if not result:
                print("Inventory not found.")
                return

            current_qty = result[0]

            cursor = self.connection.cursor()

            # Delete if quantity becomes zero or negative
            if current_qty - quantity <= 0:
                cursor.execute(
                    "DELETE FROM inventory "
                    "WHERE location = %s AND upid = %s AND expiration = %s",
                    (location, upid, expiration)
                )
            else:
                cursor.execute(
                    "UPDATE inventory SET quantity = quantity - %s "
                    "WHERE location = %s AND upid = %s AND expiration = %s",
                    (quantity, location, upid, expiration)
                )

            self.connection.commit()
            cursor.close()

            logManage(self.connection).logEntry(
                userid,
                location,
                f"Removed {quantity} of {upid}"
            )

        except mysql.connector.Error as err:
            print(f"Inventory Remove Error: {err}")
            self.connection.db.rollback()

    def invRetrieve(self, amount=10, offset=0):
        """
        Retrieves inventory records.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM inventory "
                "ORDER BY expiration DESC LIMIT %s OFFSET %s",
                (amount, offset)
            )
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Inventory Retrieve Error: {err}")
            return None


# --------------------------------------------------
# Logging
# --------------------------------------------------

class logManage:
    """
    Handles application logging.
    """

    def __init__(self, connection):
        self.connection = connection

    def logEntry(self, user, location, data):
        """
        Inserts a log entry.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO logs (uid, user, date, location, data) "
                "VALUES (%s, %s, %s, %s, %s)",
                (str(uuid.uuid4()), user, date.today(), location, data)
            )
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(f"Log Error: {err}")
            self.connection.db.rollback()

    def logRetrieve(self, amount=10, offset=0):
        """
        Retrieves logs.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM logs ORDER BY date DESC LIMIT %s OFFSET %s",
                (amount, offset)
            )
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Log Retrieve Error: {err}")
            return None


# --------------------------------------------------
# User Management
# --------------------------------------------------

class userManage:
    """
    Handles user creation, authentication, and history tracking.
    """

    def __init__(self, connection):
        self.connection = connection

    def userEntry(self, username, password):
        """
        Creates a new user.
        """
        if self.userCheck(username=username):
            print("User already exists.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (userid, username, password, auth, history) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    str(uuid.uuid4()),
                    username,
                    password,
                    "",
                    json.dumps({"history": []})
                )
            )
            self.connection.commit()
            cursor.close()

            logManage(self.connection).logEntry(
                "system",
                "userData",
                f"Registered new user: {username}"
            )

            return True

        except mysql.connector.Error as err:
            print(f"User Insert Error: {err}")
            self.connection.db.rollback()
            return None

    def userCheck(self, username="", userid=""):
        """
        Checks if a user exists.
        """
        try:
            cursor = self.connection.cursor()

            if username:
                cursor.execute(
                    "SELECT userid FROM users WHERE username = %s",
                    (username,)
                )
            elif userid:
                cursor.execute(
                    "SELECT userid FROM users WHERE userid = %s",
                    (userid,)
                )
            else:
                return False

            exists = cursor.fetchone() is not None
            cursor.close()
            return exists

        except mysql.connector.Error as err:
            print(f"User Check Error: {err}")
            return False

    def login(self, username, password):
        """
        Authenticates a user.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT userid FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else False

        except mysql.connector.Error as err:
            print(f"Login Error: {err}")
            return None

    def historyRetrieve(self, userid):
        """
        Retrieves user history JSON.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT history FROM users WHERE userid = %s",
                (userid,)
            )
            result = cursor.fetchone()
            cursor.close()
            return json.loads(result[0]) if result else None

        except mysql.connector.Error as err:
            print(f"History Retrieve Error: {err}")
            return None

    def historyUpdate(self, userid, desc, entry_date=date.today()):
        """
        Appends a history entry.
        """
        history = self.historyRetrieve(userid) or {"history": []}

        history["history"].append({
            "date": str(entry_date),
            "description": desc
        })

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE users SET history = %s WHERE userid = %s",
                (json.dumps(history), userid)
            )
            self.connection.commit()
            cursor.close()

            logManage(self.connection).logEntry(
                "system",
                "userData",
                f"Updated history for user {userid}"
            )

            return True

        except mysql.connector.Error as err:
            print(f"History Update Error: {err}")
            self.connection.db.rollback()
            return None
# End of classTypes.py