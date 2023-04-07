import pyperclip
from functions.my_functions import extract_data

clipboard_data = str(pyperclip.paste())

if clipboard_data: # just in case clipboard is empty
    data = extract_data(clipboard_data)

    if data: # copy to clipboard if data was returned
        pyperclip.copy(data)
        print("The extracted data has been copied to your clipboard")
else:
    print("No data detected")
