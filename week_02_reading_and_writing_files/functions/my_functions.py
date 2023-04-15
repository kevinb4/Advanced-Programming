import os
import shutil
import platform

def copy_file(file, file_path_from, file_path_to, is_subfile=False):
    """Copies a file from one folder to another while ensuring the file isn't larger than a GB and skips files
    Arguments:
        file [string] -- the name of the file
        file_path_from [string] -- the full path to the file being copied from
        file_path_to [string] -- the full path to the file being copied to"""
    path_to = os.path.dirname(file_path_to) # get the path to the folder where the file is being copied to

    if is_subfile:
        path_to = os.path.split(path_to)[0] # remove the subfolder for logs so they are recoreded in the main directory

    if not os.path.isfile(file_path_from): # don't copy folders
        write_log(path_to, f"{file_path_from} was skipped")
    elif os.path.getsize(file_path_from) < (1024 * 1024 * 1024): # 1GB = 1024^3 = 1,073,741,824 bytes (getsize is in bytes)
        try: # in case something goes wrong with the copy (like lack of permissions)
            shutil.copy(file_path_from, file_path_to)
            write_log(path_to, f"{file} was successfully copied to {file_path_to}")
        except:
            write_log(path_to, f"{file} could not be copied")
    else:
        write_log(path_to, f"{file} was skipped over for being over 1GB in size")

def get_folder_path(path_type):
    """Obtains the data and verifies it
    Arguments:
        path_type [string] -- the type of path to get
    Returns:
        path [string] -- the verified path"""
    data = input(f"Enter the path you want to copy files {path_type}: ")
    data_ok = False

    while not data_ok:
        path = os.path.join(get_root(), data) # take the root and merge it with the folder entered
        error = ""

        if path_type == "from":
            if is_valid_path(path): # if the path exists and is not empty
                data_ok = True
            else:
                error = "The specified folder does not exist, please enter an existing path: "
        elif path_type == "to":
            if not os.path.exists(path):
                os.makedirs(path) # make the folder if it does not exist
                write_log(path, f"{path} was created successfully")
                data_ok = True
            elif path_empty(path): # if the folder exists and is empty, it's ok
                data_ok = True 
            else:
                error = "The path specified to copy files to exists and contains files. Please specify an empty directory: "

        if not data_ok:
            data = input(error)

    return path

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

def is_valid_path(path):
    """Checks if the path is valid and has files it it
    Arguments:
        path [string] -- the path to be checked
    Returns:
        true/false [boolean] -- whether or not the path is valid or not"""
    return os.path.exists(path) and not path_empty(path)

def path_empty(path):
    """Returns whether the path is empty or not
    Arguments:
        path [string] -- the path to be checked
    Returns:
        true/false [boolean] -- whether or not the path is empty or not"""
    try: # in case the directory does not exist
        if len(os.listdir(path)) == 0:
            return True # true because the path is empty
        else:
            return False # false because the path is not empty
    except:
        return True # true because the path does not exist, so it's therefore empty

def process_files(path_from, path_to):
    """Processes all files in a directory under 1GB
    Arguments:
        path_from [string] -- the path where the files will be copied from
        path_to [string] -- the path where the files will be copied to"""
    files = os.listdir(path_from)

    for file in files:
        file_path_from = os.path.join(path_from, file) # get the full path to the file is currently at
        file_path_to = os.path.join(path_to, file) # get the full path to where the file is being moved

        if os.path.isfile(file_path_from):
            copy_file(file, file_path_from, file_path_to)
        else: # handle subfolders only in the root directory
            subfiles = os.listdir(file_path_from) # get all the files in the subfolder

            if not os.path.exists(file_path_to): # path needs to exist before files can be copied
                os.makedirs(file_path_to) # make the folder if it does not exist
                write_log(path_to, f"{file_path_to} was created successfully") # write log file in destination root
            
            for subfile in subfiles:
                subfile_path_from = os.path.join(file_path_from, subfile) # get the full path to the subfile
                subfile_path_to = os.path.join(file_path_to, subfile) # get the full path to the destination subfile

                copy_file(subfile, subfile_path_from, subfile_path_to, True)

def write_log(path, text):
    """Writes to the log file
    Arguments:
        path [string] -- where the log file will be written
        text [string] -- the message to be written in the log file"""
    with open(os.path.join(path, "log.txt"), "a") as log:
        log.write(f"{text}\n")