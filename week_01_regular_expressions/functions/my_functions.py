import re

def build_data(coords, dollars, ccs):
    """Builds the data together in the requested format
    Arguments:
        coords [list] -- list of all the coords from the data import
        dollars [list] -- list of all the dollars from the data import
        ccs [list] -- list of all the credit cards from the data import
    Returns:
        data [string] -- formatted data"""
    data = "Coord | Dollars | CC_Num\n"

    # ensure all match before running by matching lengths
    if len(coords) == len(dollars) and len(coords) == len(ccs):
        for count in range(len(coords)):
            data += f"{coords[count]} | {dollars[count]} | {ccs[count]}\n"
    else:
        print("Data is not consistent - unable to process")
        return False

    return data[:-1] # remove last new line

def combine(data):
    """Returns the combined list from the passed tuple
    Arguments:
        data [tuple] -- raw data passed from regex
    Returns:
        data_list [list] -- list of the data connected"""
    data_list = []

    for record in data:
        temp_line = ""
        for item in record:
            temp_line += str(item)
        data_list.append(temp_line)

    return data_list

def extract_data(data):
    """Returns the extracted data from the passed data
    Arguments:
        data [string] -- passed data from the clipboard
    Returns:
        extracted_data [array] -- """
    re_coord = re.compile(r"(-?\d{1,3}?\.\d+), (-?\d{1,3}?\.\d+)")
    re_money = re.compile(r"\$\d,\d{3}?")
    re_cc = re.compile(r"(?:\d ?){13,19}")

    ex_coord = combine(re_coord.findall(data)) # combine results that have groups
    ex_money = re_money.findall(data)
    ex_cc = combine(re_cc.findall(data)) # combine results that have groups

    # if no data was extracted return false
    if len(ex_coord) == 0 or len(ex_money) == 0 or len(ex_cc) == 0:
        print("Incorrect data on clipboard")
        return False

    return build_data(ex_coord, ex_money, ex_cc)

def validate_cc(passed_value):
    """Validates credit cards
    Arguments:
        passed_value [string] -- input to validate
    Returns:
        true/false [boolean] -- whether or not the credit card passed is valid"""
    re_cc = re.compile(r"(?:\d ?){13,19}")
    test = re_cc.search(passed_value)

    if test is None:
        return False
    else:
        if passed_value == test.group(): # ensure nothing else was added to the value
            return True
        else:
            return False

def validate_coords(passed_value):
    """Validates coordinates
    Arguments:
        passed_value [string] -- input to validate
    Returns:
        true/false [boolean] -- whether or not the coords passed are valid"""
    re_coord = re.compile(r"(-?\d{1,3}?\.\d+), (-?\d{1,3}?\.\d+)")
    test = re_coord.search(passed_value)

    if test is None:
        return False
    else:
        if passed_value == test.group(): # ensure nothing else was added to the value
            return True
        else:
            return False
        
def validate_money(passed_value):
    """Validates money
    Arguments:
        passed_value [string] -- input to validate
    Returns:
        true/false [boolean] -- whether or not the money passed is valid"""
    re_money = re.compile(r"\$\d,\d{3}?")
    test = re_money.search(passed_value)

    if test is None:
        return False
    else:
        if passed_value == test.group(): # ensure nothing else was added to the value
            return True
        else:
            return False