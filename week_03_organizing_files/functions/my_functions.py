import os
import re
import shutil
import zipfile
import platform
import send2trash

def copy_file(source, destination):
    """Copies a file to a destination with basic error handling
    Arguments:
        source [string] -- the path of the file to be copied
        destination [string] -- the path where the file will be copied to"""
    if not os.path.isfile(source):
        print("Source file was not found")
        return

    if os.path.exists(destination):
        print("Destination file already exists")
        return

    try:
        os.makedirs(os.path.dirname(destination))
        shutil.copy(source, destination)
    except:
        print("An error occurred while copying the file")

def find_ips(path):
    """Finds the ips of the specified lines in the log files
    Arguments:
        path [string] -- the path of the file to be filtered
    Returns:
        entries [list] -- a list of ips found in the file"""
    if not os.path.isfile(path):
        print("File was not found")
        return

    try:
        entries = []

        with open(path, "r") as file:
            lines = file.readlines() # read all file lines into a list
            for line in lines:
                if re.search(r"(\.\.\/)|(\/wp-login\.php\?action=register)|(403 HTTP)|(install)|(select)", line):
                    ip = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line).group(0) # grab the source ip (first ip listed via the group) from the line

                    if ip not in entries: # no duplicate ips (it makes sense if the same ip is found on different sites however)
                        entries.append(ip)
                        write_log(os.path.join(get_root(), "logs", "matches.txt"), f"{ip},{os.path.basename(path)}") # write the ip and the filename to a file

        return entries
    except:
        print("An error occurred while running the filter")

def get_root():
    """Returns the correct path depending on the operating system
    Returns:
        root [string] -- the start of the path depending on the OS"""
    root = ""

    if platform.system() == "Windows":
        root = "C:\\"
    else:
        root = "/"

    return root

def process_logs(path):
    """Processes the log files and extracts the ips, then writes the results
    Arguments:
        path [string] -- the path of the folder containing the log files"""
    for item in os.walk(path):
        for filename in item[2]:
            ips = find_ips(os.path.join(item[0], filename)) # process each log file and extracts ips of specified lines
            
            if len(ips) > 0:
                os.rename(os.path.join(item[0], filename), os.path.join(item[0], f"processed_{filename}")) # renames each log file with "processed_" prefix
            else:
                send2trash.send2trash(item[0]) # sends files that don't have any matches to the recycle bin using Send2Trash, along with its parent folder

def unzip_file(file, path):
    """Unzips a file
    Arguments:
        file [string] -- the file to be unzipped
    Returns:
        true/false [bool] -- whether the file was unzipped successfully or not"""
    if not os.path.isfile(file):
        print("The zip file was not found, aborting...")
        return False
    
    if os.path.exists(path):
        print("The zip extraction destination already exists, aborting...")
        return False

    try:
        with zipfile.ZipFile(file, "r") as zip:
            zip.extractall(path)
            return True
    except:
        print("An error occurred while unzipping the file")

def write_log(path, text):
    """Writes to the log file
    Arguments:
        path [string] -- where the log file will be written
        text [string] -- the message to be written in the log file"""
    with open(path, "a") as log:
        log.write(f"{text}\n")

def zip_logs(path):
    """Zips the log files in the running directory text_files folder
    Arguments:
        path [string] -- the path of the folder containing the log files"""
    if not os.path.isdir(path):
        print("Directory was not found")
        return

    try:
        with zipfile.ZipFile("text_files/results.zip", "w") as zip:
            for item in os.walk(path):
                for filename in item[2]:
                    zip.write(os.path.join(item[0], filename), compress_type=zipfile.ZIP_DEFLATED)
    except:
        print("An error occurred while zipping the files")