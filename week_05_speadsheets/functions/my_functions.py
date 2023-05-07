import requests
import os
from bs4 import BeautifulSoup
from openpyxl.styles import Font
from openpyxl.styles import Alignment

def format_excel(sheet):
    """Format the excel sheet
    Arguments:
        sheet [object] -- the excel sheet to format"""
    sheet.title = "Office Supplies"

    sheet["A1"] = "Sales Data"
    sheet["A2"] = "Product"
    sheet["B2"] = "Quantity"
    sheet["C2"] = "Orders"
    sheet["D2"] = "Average"

    sheet["A1"].font = Font(b=True, color="000000FF")
    sheet["A1"].alignment = Alignment(horizontal="center")

    bold = Font(b=True)

    sheet["A2"].font = bold
    sheet["B2"].font = bold
    sheet["C2"].font = bold
    sheet["D2"].font = bold

    sheet.merge_cells("A1:D1")

def get_sales_data():
    """Get the sales data from the website
    Returns:
        BeautifulSoup [object] -- the sales data"""
    # do not keep downloading the file over and over again
    if not os.path.isfile("downloads/sales_data.html"):
        request = requests.get("https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week05/WI20-Assignment/sales_data.html")

        if request.status_code == 200:
            data = open("downloads/sales_data.html", "wb")

            for data_chunk in request.iter_content(100000):
                data.write(data_chunk)

    # open html file to parse its data
    sales = open("downloads/sales_data.html", encoding="utf8")
    
    return BeautifulSoup(sales, "lxml")

def insert_excel_data(items, sheet):
    """Insert the data into the excel sheet
    Arguments:
        items [list] -- the list of dicts containing the data
        sheet [object] -- the excel sheet to insert the data into
    Returns:
        sheet [object] -- the excel sheet with the data inserted"""
    # start under the first two rows
    row = 3

    for item in items:
        sheet.cell(row=row, column=1).value = item['name']
        sheet.cell(row=row, column=2).value = item['quantity']
        sheet.cell(row=row, column=3).value = item['count']
        sheet.cell(row=row, column=4).value = f"=B{row}/C{row}"

        row += 1

    return sheet

def insert_google_data(items, sheet):
    """Insert the data into the google sheet
    Arguments:
        items [list] -- the list of dicts containing the data
        sheet [object] -- the google sheet to insert the data into
    Returns:
        rows [list] -- the rows with the data inserted"""
    rows = sheet.getRows()

    rows[0][0] = "Sales Data"
    rows[1][0] = "Product"
    rows[1][1] = "Quantity"
    rows[1][2] = "Orders"
    rows[1][3] = "Average"

    row = 2 # google is 0 indexed

    for item in items:
        rows[row][0] = item['name']
        rows[row][1] = item['quantity']
        rows[row][2] = item['count']
        rows[row][3] = f"=B{row + 1}/C{row + 1}" # account for google being 0 indexed

        row += 1

    return rows

def scrape_data(rows):
    """Scrape the data from the website
    Arguments:
        rows [list] -- the rows of data to scrape
    Returns:
        items [list] -- the list of dicts containing the data"""
    items = []

    # grab item name and quantity totals
    for row in rows:
        data = row.find_all("td")
        name = data[3].getText().strip()
        quantity = data[4].getText().strip()
        found = False

        # skip the heading
        if not quantity.isdigit():
            continue

        # loop through item dicts to see if item already exists
        for item in items:
            if name in item.values():
                item['quantity'] += int(quantity)
                item['count'] += 1 # update the count for averages
                found = True

        # if item does not exist, add it to the list
        if not found:
            items.append({'name': name, 'quantity': int(quantity), 'count': 1})

    return items