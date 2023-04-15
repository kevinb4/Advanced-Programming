from functions.my_functions import get_folder_path, process_files

path_from = get_folder_path("from")
path_to = get_folder_path("to")

process_files(path_from, path_to)