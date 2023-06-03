import os
import json
from datetime import datetime
from functions.my_functions import *

# if script is running from a task scheduler, the working directory needs to be changed to the project folder
if not os.path.exists("text_files"):
    os.chdir(os.path.dirname(__file__))

with open("text_files/script_config.json") as file:
    config = json.load(file)

# always run alert checks
alert_check(config)

hhmm = datetime.now().strftime('%H:%M')

# send out email reports at 6am and 6pm
if hhmm == "06:00" or hhmm == "18:00":
    handle_email_report(config)