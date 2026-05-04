import classTypes
import datetime

def printTable(headers, data):
    str_data = [[str(item) for item in row] for row in data]
    str_headers = [str(h) for h in headers]

    all_rows = [str_headers] + str_data
    col_widths = [
        max(len(row[i]) for row in all_rows)
        for i in range(len(headers))
    ]

    def format_row(row):
        return " | ".join(
            row[i].ljust(col_widths[i]) for i in range(len(row))
        )
    print(format_row(str_headers))
    print("-+-".join('-' * w for w in col_widths))

    for row in str_data:
        print(format_row(row))

def get_db():
    """Loads config and returns an active dbConnection."""

    dbConnect = classTypes.dbConnection(
        "jjs-mis.tail6e1087.ts.net",
        "testuser",
        "Colorado13!",
        "inv",
        3306
    )

    dbConnect.initiate()  # No args accepted
    dbConnect.cursor()  # No args accepted
    if dbConnect:
        return dbConnect
    
def viewInventory(invManager):
    """Returns a list of all medications in the inventory."""
    print("Current Inventory:")
    printTable(headers = ["ID", "Location", "Amount", "Date", "Item"]
         , data = invManager.invRetrieve())
    
def viewLogs(logManager):
    """Returns a list of all medications in the inventory."""
    print("Current Logs:")
    printTable(headers = ["ID", "User", "Date", "Location", "Data"]
         , data = logManager.logRetrieve())
    
def updateInventory(invManager):
    """Updates the inventory based on user input."""
    print("Update Inventory:")
    userid = input("Enter user ID: ")
    upid = input("Enter Product ID: ")
    location = input("Enter location: ")
    quantity = input("Enter quantity: ")
    year = int(input("Enter expiration year: "))
    month = int(input("Enter expiration month: "))
    day = int(input("Enter expiration day: "))
    name = input("Enter item name: ")
    invManager.invEntry(userid, upid, location, int(quantity), datetime.datetime(year, month, day), name)
    print("Inventory updated.")

def updateRmvInventory(invManager):
    """Updates the inventory based on user input."""
    print("Update Inventory:")
    userid = input("Enter user ID: ")
    upid = input("Enter Product ID: ")
    location = input("Enter location: ")
    quantity = input("Enter quantity: ")
    year = int(input("Enter expiration year: "))
    month = int(input("Enter expiration month: "))
    day = int(input("Enter expiration day: "))
    name = input("Enter item name: ")
    invManager.invRemove(userid, upid, location, int(quantity), datetime.datetime(year, month, day))
    print("Inventory updated.")

if __name__ == "__main__":
    db = get_db()
    invManager = classTypes.invManage(db)
    logManager = classTypes.logManage(db)
    print("-"*40)
    print("Options:")
    print("1. View Inventory")
    print("2. View Logs")
    print("3. Add Inventory")
    print("4. Remove Inventory")
    choice = int(input("Select an option: "))
    if choice == 1:
        viewInventory(invManager)
    elif choice == 2:
        viewLogs(logManager)
    elif choice == 3:
        updateInventory(invManager)
    elif choice == 4:
        updateRmvInventory(invManager)
    db.close()