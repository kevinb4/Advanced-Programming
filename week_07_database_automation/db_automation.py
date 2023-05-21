import os
from functions.my_functions import *
from classes.database_access import DB_Connect

db = DB_Connect("root", "1234", "python_projects")
extensions = ['csv', 'json', 'xml'] # valid file extensions
found = False

while not found:
    file_name = input("Enter the name of the file you want to import that's located in the text_files folder: ")
    file_path = f"text_files/{file_name}"
    extension = get_ext(file_path)
    error = ""

    # check if the file exists and a valid extention was found
    if os.path.isfile(file_path) and extension:
        # check for valid extension
        if extension in extensions:
            found = True
        else:
            error = "Invalid file extension. Please try again."
    else:
        error = "File not found. Please try again."

    if error:
        print(error)

if extension == "csv":
    addresses = read_csv(file_path)
elif extension == "json":
    addresses = read_json(file_path)
elif extension == "xml":
    addresses = read_xml(file_path)

for address in addresses:
    db.executeQuery("INSERT INTO addresses_working (first_name, last_name, street, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s)", (address["first_name"], address["last_name"], address["street"], address["city"], address["state"], address["zip"]))

try:
    db.executeQuery("START TRANSACTION")
    db.executeQuery("RENAME TABLE python_projects.addresses TO python_projects.addresses_backup") # rename the current table
    db.executeQuery("RENAME TABLE python_projects.addresses_working TO python_projects.addresses") # rename the working table with the new data
    db.executeQuery("RENAME TABLE python_projects.addresses_backup TO python_projects.addresses_working") # set the old table as the working table so this app can be ran again
    db.executeQuery("COMMIT")

    print("File imported successfully!")
except:
    print("There was an error importing the file. Please try again.")