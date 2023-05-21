import os
import json
from bs4 import BeautifulSoup

def get_ext(file_name):
    """Returns the file extension or false if there is no extension
    Arguments:
        file_name [string] -- the name of the file
    Returns:
        extension [string] -- the file extension or false if there is no extension"""
    try:
        extension = os.path.basename(file_name).split(".")[1]
    except:
        extension = False

    return extension

def read_csv(directory):
    """Reads a csv file and returns the data
    Arguments:
        directory [string] -- the path to the file
    Returns:
        addresses [list] -- a list of dictionaries containing the addresses"""
    with open(directory) as file:
        data = file.readlines()

    addesses = []

    for line in data:
        line = line.strip().split(",")

        # skip the header
        if line[0] == "first_name":
            continue

        addesses.append({"first_name": line[0], "last_name": line[1], "street": line[2], "city": line[3], "state": line[4], "zip": line[5]})

    return addesses

def read_json(directory):
    """Reads a json file and returns the data
    Arguments:
        directory [string] -- the path to the file
    Returns:
        addresses [list] -- a list of dictionaries containing the addresses"""
    with open(directory) as file:
        data = json.load(file)

    addresses = []

    for item in data:
        addresses.append({"first_name": item["first_name"], "last_name": item["last_name"], "street": item["street"], "city": item["city"], "state": item["state"], "zip": item["zip"]})

    return addresses

def read_xml(directory):
    """Reads a xml file and returns the data
    Arguments:
        directory [string] -- the path to the file
    Returns:
        addresses [list] -- a list of dictionaries containing the addresses"""
    with open(directory, encoding="utf-8") as file:
        data = file.read()
    
    xml = BeautifulSoup(data, "xml")
    entries = xml.find_all("entry")
    addresses = []

    for entry in entries:
        addresses.append({"first_name": entry.first_name.get_text(), "last_name": entry.last_name.get_text(), "street": entry.street.get_text(), "city": entry.city.get_text(), "state": entry.state.get_text(), "zip": entry.zip.get_text()})

    return addresses