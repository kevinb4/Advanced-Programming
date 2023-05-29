import os
import ezsheets
import requests
import openpyxl
from datetime import datetime

def download_data():
    """Download the data from the website and save it to a file
    Returns:
        lines [list] -- a list of strings, each string is a line from the file"""
    # it's good practice not to make so many requests to a website, but since the data may be updated frequently, it will be downloaded every time
    request = requests.get("https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week08/WI20-Assignment/exam_data.csv")

    if request.status_code == 200:
        exam_data = open("text_files/exam_data.csv", "wb")

        for data in request.iter_content(100000):
            exam_data.write(data)

    # open file and parse the data
    with open("text_files/exam_data.csv", "r") as file:
        lines = file.readlines()

    return lines

def parse_data(lines):
    """Parses the data from the file
    Arguments:
        lines [list] -- a list of strings, each string is a line from the file
    Returns:
        data [list] -- a list of lists, each list is a row of data from the file"""
    # create a list of lists which hold the data
    # typically I'd use a dict but doing it this way makes it more flexible if different data is added
    data = []

    for line in lines:
        line = line.split(",")
        line_data = []
        for item in line:
            line_data.append(item.strip())
        data.append(line_data)
    
    return data

def process_db(db, data):
    """Process the data and saves it to a database
    Arguments:
        db [object] -- a database connection object
        data [list] -- a list of lists, each list is a row of data from the file"""
    # typically the data would be built in a string and inserted all at once,
    # but since this assignment is about threading I'm inserting each row individually
    try:
        # dump any current data in the database
        db.executeQuery("DELETE FROM exam_data")
        db.conn.commit()

        for item in data[1:]: # skip the first row since it's the header
            db.executeQuery("INSERT INTO exam_data (parental_education, test_prep_course, math_score, reading_score, writing_score) VALUES (%s, %s, %s, %s, %s)", (item[0], item[1], item[2], item[3], item[4]))
        db.conn.commit()
        write_log("The database import is complete")
    except:
        write_log("The database import failed")  

def process_excel(data):
    """Process the data and saves it to an excel workbook
    Arguments:
        data [list] -- a list of lists, each list is a row of data from the file"""
    # create the excel workbook
    excel_workbook = openpyxl.Workbook()
    excel_sheet = excel_workbook.active

    # insert the data into the excel sheet
    row = 1
    for item in data:
        column = 1
        for value in item:
            excel_sheet.cell(row=row, column=column, value=value)
            column += 1
        row += 1

    try:
        # save the excel workbook
        excel_workbook.save("text_files/exam_data.xlsx")
        write_log("The excel workbook import is complete")
    except:
        write_log("The excel workbook import failed")

def process_google(data):
    """Process the data and saves it to a google sheet
    Arguments:
        data [list] -- a list of lists, each list is a row of data from the file"""
    try:
        # create a new spreadsheet
        # google_workbook = ezsheets.createSpreadsheet("Exam Data")

        # use the spreadsheet created above
        google_workbook = ezsheets.Spreadsheet('1AWhRM-oLDMmCsH2G8sIdav0JpqAYJfAWjpqNAS4AdFF')
        google_sheet = google_workbook[0]
        rows = google_sheet.getRows()

        # insert the data into the google sheet
        row = 1
        for item in data:
            column = 1
            for value in item:
                rows[row, column] = value
                column += 1
            row += 1

        # update the google sheet with the rows
        google_sheet.updateRows(rows)
        write_log("The google sheet import is complete")
    except:
        write_log("The google sheet import failed")  

def write_log(message):
    """Writes the log file with a formatted timestamp
    Arguments:
        message [string] -- the message to write to the log file"""
    # seems like datetime formatting doesn't have an option to not include the 0 for the day/hour so I used replace to get rid of it
    # the leading 0 will also be removed for 24 hour time, which might look odd at midnight, but this is how the formatting example looks
    with open("text_files/script_log.txt", "a") as log:
        log.write(f"{datetime.now().strftime('%B %d, %Y %H:%M:%S').replace(' 0', ' ')} - {message}\n")