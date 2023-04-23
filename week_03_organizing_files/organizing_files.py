import os
from functions.my_functions import *

# define paths to make them easily customizable
logs_path = os.path.join(get_root(), "logs")
access_logs_zip_path = os.path.join(get_root(), "log_processing", "access_logs.zip")

# copy file to root in a folder called log_processing
copy_file("text_files/access_logs.zip", access_logs_zip_path)

# unzip data from the file in a folder called logs in the root
result = unzip_file(access_logs_zip_path, logs_path)

# if the file wasn't unzipped successfully, there's no point in running any further since it risks deleting the wrong files
if result:
    # process the log files with specific search patterns and extracting ips, then write the results to a file
    process_logs(logs_path)

    # zip the log files and move them back to running directory
    zip_logs(logs_path)