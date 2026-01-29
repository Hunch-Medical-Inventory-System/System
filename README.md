<<<<<<< HEAD
# System
=======
# Database Management Module
To ease usage

## Requirements
- Python 3.9+
- MySQL Server
- Python package:
  ```bash
  pip install mysql-connector-python
  ```

## Usage

### Setup
Python Usage
```python
import classTypes as CT  # references classTypes.py
import datetime  # to adjust dates 
data = CT.parseJSON('connect.json')  # where connectinfo is stored
dbConnect = CT.dbConnection(
    data['connectioninfo'][0]['host'],
    data['connectioninfo'][0]['user'],
    data['connectioninfo'][0]['password'],
    data['connectioninfo'][0]['database'],
    data['connectioninfo'][0]['port']
)
dbConnect.initiate()  # turns connect on
# Put code here
dbConnect.close()  # disconnects
```

connect.json
```json
{
  "connectioninfo": [
    {
      "host": "###",
      "user": "###",
      "password": "###",
      "database": "###",
      "port": 3306
    }
  ]
}
```

---

### parseJSON
Utility function to parse JSON files

Calling function
```python
data = CT.parseJSON('connect.json')  # filename as string
```

Parameters:
- `filename` (str): Path to the JSON file to parse

Outputs:
- Returns parsed JSON data as dictionary/list
- Returns `None` if file not found, JSON is malformed, or other errors occur
- Prints appropriate error messages

---

### dbConnection
Manages database connection

Calling function
```python
dbConnect = CT.dbConnection(
    data['connectioninfo'][0]['host'],      # host ip
    data['connectioninfo'][0]['user'],      # username
    data['connectioninfo'][0]['password'],  # password
    data['connectioninfo'][0]['database'],  # database name
    data['connectioninfo'][0]['port']       # port number
)
```

#### initiate
```python
dbConnect.initiate()  # No args accepted
```
Starts the connection with the SQL server

Outputs:
- `True`: successfully connected
- `False`: failed to connect (prints errors)

#### cursor
```python
dbConnect.cursor()  # No args accepted
```
Returns the SQL cursor

Outputs:
- The DB Cursor to interact with the database

#### commit
```python
dbConnect.commit()  # No args accepted
```
Commits the SQL Cursor's actions

Outputs:
- None

#### close
```python
dbConnect.close()  # No args accepted
```
Closes the connection with the SQL Server

Outputs:
- None

---

### invManage
Manages inventory operations

Calling function
```python
inventory = CT.invManage(dbConnect)  # pass dbConnection object
```

#### invEntry
```python
inventory.invEntry(userid, upid, location, quantity, expiration, name)
```
Adds a new inventory entry to the database

Parameters:
- `userid` (str): User ID performing the action
- `upid` (str): Universal Product ID
- `location` (str): Storage location
- `quantity` (int): Quantity of items
- `expiration` (date): Expiration date
- `name` (str): Product name

Outputs:
- Prints "Data inserted successfully." on success
- Prints error message on failure
- Creates a log entry automatically

#### invRemove
```python
inventory.invRemove(userid, upid, location, quantity, expiration)
```
Removes inventory from the database

Parameters:
- `userid` (str): User ID performing the action
- `upid` (str): Universal Product ID
- `location` (str): Storage location
- `quantity` (int): Quantity to remove
- `expiration` (date): Expiration date

Outputs:
- If quantity to remove equals or exceeds current quantity: deletes entire entry
- If quantity to remove is less than current: updates quantity
- Prints status message
- Creates a log entry automatically
- Returns `None` if no inventory found at location

#### invRetrieve
```python
results = inventory.invRetrieve(amount=10, offset=0)
```
Retrieves inventory entries from the database

Parameters:
- `amount` (int, optional): Number of records to retrieve (default: 10)
- `offset` (int, optional): Number of records to skip (default: 0)

Outputs:
- Returns list of tuples containing inventory records, ordered by expiration date (descending)
- Returns `None` on error

---

### logManage
Manages system logging

Calling function
```python
logs = CT.logManage(dbConnect)  # pass dbConnection object
```

#### logData
```python
formatted_desc = logs.logData(desc)
```
Formats log description (currently returns input as-is)

Parameters:
- `desc` (str): Description to format

Outputs:
- Returns the description string

#### logEntry
```python
logs.logEntry(user, location, data)
```
Creates a new log entry in the database

Parameters:
- `user` (str): User ID or "system" for system actions
- `location` (str): Location or category of the action
- `data` (str): Description of the action

Outputs:
- Prints "Data inserted successfully." on success
- Prints error message on failure
- Automatically generates unique ID (UUID) and current date

#### logRetrieve
```python
results = logs.logRetrieve(amount=10, offset=0)
```
Retrieves log entries from the database

Parameters:
- `amount` (int, optional): Number of records to retrieve (default: 10)
- `offset` (int, optional): Number of records to skip (default: 0)

Outputs:
- Returns list of tuples containing log records, ordered by date (descending)
- Returns `None` on error

---

### userManage
Manages user operations

Calling function
```python
users = CT.userManage(dbConnect)  # pass dbConnection object
```

#### userEntry
```python
result = users.userEntry(username, password)
```
Registers a new user in the database

Parameters:
- `username` (str): Username for the new user
- `password` (str): Password for the new user

Outputs:
- Returns user record if user already exists
- Returns `None` if successfully created (also prints "Data inserted successfully.")
- Returns `None` on error
- Creates a log entry automatically
- Automatically generates unique user ID (UUID) and empty history

#### userCheck
```python
exists = users.userCheck(username="", userid="")
```
Checks if a user exists in the database

Parameters:
- `username` (str, optional): Username to check (default: "")
- `userid` (str, optional): User ID to check (default: "")

Note: Provide either username OR userid, not both

Outputs:
- `True`: user exists
- `False`: user does not exist
- `None`: error occurred

#### historyJSON
```python
json_data = users.historyJSON(date=date.today(), desc="No Description Inserted")
```
Creates a JSON formatted history entry

Parameters:
- `date` (date, optional): Date of the history entry (default: today)
- `desc` (str, optional): Description of the history entry (default: "No Description Inserted")

Outputs:
- Returns JSON string with date and description

#### login
```python
userid = users.login(username, password)
```
Authenticates a user

Parameters:
- `username` (str): Username
- `password` (str): Password

Outputs:
- Returns user ID (first element of user record) if credentials are valid
- Returns `False` if credentials are invalid
- Returns `None` on error

#### historyRetrieve
```python
history = users.historyRetrieve(userid)
```
Retrieves user history from the database

Parameters:
- `userid` (str): User ID

Outputs:
- Returns dictionary containing user history
- Returns `None` if user has no history or on error
- Creates a log entry automatically

#### historyUpdate
```python
success = users.historyUpdate(userid, date=date.today(), desc="No Description Inserted")
```
Updates user history in the database

Parameters:
- `userid` (str): User ID
- `date` (date, optional): Date of the history entry (default: today)
- `desc` (str, optional): Description of the history entry (default: "No Description Inserted")

Outputs:
- `True`: history updated successfully
- `None`: user doesn't exist or error occurred
- Creates a log entry automatically

---

## Database Schema

### inventory table
Expected columns:
- `upid` (str): Universal Product ID
- `location` (str): Storage location
- `quantity` (int): Item quantity
- `expiration` (date): Expiration date
- `name` (str): Product name

### logs table
Expected columns:
- `uid` (str): Unique log ID (UUID)
- `user` (str): User ID or "system"
- `date` (date): Log date
- `location` (str): Location/category
- `data` (str): Log description

### users table
Expected columns:
- `userid` (str): Unique user ID (UUID)
- `username` (str): Username
- `password` (str): Password
- `auth` (str): Authorization level
- `history` (JSON str): User history data

---

## Example Usage

```python
import classTypes as CT
from datetime import date, timedelta

# Setup connection
data = CT.parseJSON('connect.json')
dbConnect = CT.dbConnection(
    data['connectioninfo'][0]['host'],
    data['connectioninfo'][0]['user'],
    data['connectioninfo'][0]['password'],
    data['connectioninfo'][0]['database'],
    data['connectioninfo'][0]['port']
)

if dbConnect.initiate():
    # User management
    users = CT.userManage(dbConnect)
    users.userEntry("john_doe", "secure_password")
    userid = users.login("john_doe", "secure_password")
    
    if userid:
        # Inventory management
        inventory = CT.invManage(dbConnect)
        expiration_date = date.today() + timedelta(days=30)
        inventory.invEntry(
            userid=userid,
            upid="PROD123",
            location="Warehouse A",
            quantity=100,
            expiration=expiration_date,
            name="Widget XYZ"
        )
        
        # Retrieve inventory
        items = inventory.invRetrieve(amount=20)
        for item in items:
            print(item)
        
        # Update user history
        users.historyUpdate(userid, date.today(), "Added 100 widgets to inventory")
        
        # Retrieve logs
        logs = CT.logManage(dbConnect)
        recent_logs = logs.logRetrieve(amount=50)
        for log in recent_logs:
            print(log)
    
    dbConnect.close()
```

---

## Notes

- All database operations include error handling with rollback on failure
- Log entries are automatically created for most inventory and user operations
- UUIDs are automatically generated for new users and log entries
- Password storage is in plain text - consider implementing hashing for production use
- The `auth` field in users table is currently unused but available for authorization levels
>>>>>>> 5426c17 (Squashed 'module/DataBase-Module/' content from commit 9badead)
