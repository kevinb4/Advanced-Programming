import os
import threading
from functions.my_functions import *
from classes.database_access import DB_Connect

db = DB_Connect("root", "1234", "python_projects")

# if script is running from a task scheduler, the working directory needs to be changed to the project folder
if not os.path.exists("text_files"):
    os.chdir(os.path.dirname(__file__))

# downloading and parsing the data needs to be done before the threads can be started
lines = download_data()
data = parse_data(lines)

excel_thread = threading.Thread(target=process_excel, args=(data,))
google_thread = threading.Thread(target=process_google, args=(data,))
db_thread = threading.Thread(target=process_db, args=(db, data,))

excel_thread.start()
google_thread.start()
db_thread.start()