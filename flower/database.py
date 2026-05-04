import classTypes
import datetime


def printTable(headers, data):
    """Pretty-prints tabular data in aligned columns."""

    # Convert all data to strings so formatting works consistently
    str_data = [[str(item) for item in row] for row in data]
    str_headers = [str(h) for h in headers]

    # Combine headers and data to compute column widths
    all_rows = [str_headers] + str_data

    # Determine maximum width needed for each column
    col_widths = [
        max(len(row[i]) for row in all_rows)
        for i in range(len(headers))
    ]

    def format_row(row):
        """Formats a single row using calculated column widths."""
        return " | ".join(
            row[i].ljust(col_widths[i]) for i in range(len(row))
        )

    # Print header row
    print(format_row(str_headers))

    # Print separator line
    print("-+-".join('-' * w for w in col_widths))

    # Print all data rows
    for row in str_data:
        print(format_row(row))


def get_db():
    """Creates and returns a database connection object."""

    dbConnect = classTypes.dbConnection(
        "jjs-mis.tail6e1087.ts.net",
        "testuser",
        "Colorado13!",
        "inv",
        3306
    )

    # Initialize connection and cursor
    dbConnect.initiate()
    dbConnect.cursor()

    # Return connection if successful
    if dbConnect:
        return dbConnect


def viewInventory(invManager):
    """Fetches and displays current inventory records."""

    print("Current Inventory:")

    # Retrieve inventory data and print in table format
    printTable(
        headers=["ID", "Location", "Amount", "Date", "Item"],
        data=invManager.invRetrieve()
    )


def viewLogs(logManager):
    """Fetches and displays system logs."""

    print("Current Logs:")

    # Retrieve log data and print in table format
    printTable(
        headers=["ID", "User", "Date", "Location", "Data"],
        data=logManager.logRetrieve()
    )


def updateInventory(invManager):
    """Adds a new inventory record based on user input."""

    print("Update Inventory:")

    # Collect user input for inventory entry
    userid = input("Enter user ID: ")
    upid = input("Enter Product ID: ")
    location = input("Enter location: ")
    quantity = input("Enter quantity: ")

    # Collect expiration date components
    year = int(input("Enter expiration year: "))
    month = int(input("Enter expiration month: "))
    day = int(input("Enter expiration day: "))

    name = input("Enter item name: ")

    # Create datetime object and insert record
    invManager.invEntry(
        userid,
        upid,
        location,
        int(quantity),
        datetime.datetime(year, month, day),
        name
    )

    print("Inventory updated.")


def updateRmvInventory(invManager):
    """Removes inventory based on user input."""

    print("Update Inventory:")

    # Collect user input for removal
    userid = input("Enter user ID: ")
    upid = input("Enter Product ID: ")
    location = input("Enter location: ")
    quantity = input("Enter quantity: ")

    # Expiration date (used for identifying item batch)
    year = int(input("Enter expiration year: "))
    month = int(input("Enter expiration month: "))
    day = int(input("Enter expiration day: "))

    name = input("Enter item name: ")

    # Remove inventory record
    invManager.invRemove(
        userid,
        upid,
        location,
        int(quantity),
        datetime.datetime(year, month, day)
    )

    print("Inventory updated.")


if __name__ == "__main__":
    """Main program entry point."""

    # Establish database connection
    db = get_db()

    # Create manager objects for inventory and logs
    invManager = classTypes.invManage(db)
    logManager = classTypes.logManage(db)

    # Display menu
    print("-" * 40)
    print("Options:")
    print("1. View Inventory")
    print("2. View Logs")
    print("3. Add Inventory")
    print("4. Remove Inventory")

    # Get user choice
    choice = int(input("Select an option: "))

    # Execute selected option
    if choice == 1:
        viewInventory(invManager)
    elif choice == 2:
        viewLogs(logManager)
    elif choice == 3:
        updateInventory(invManager)
    elif choice == 4:
        updateRmvInventory(invManager)

    # Close database connection when done
    db.close()