import ezsheets
import openpyxl
from functions.my_functions import *

# grab the sales data from the website
sales_soup = get_sales_data()

table = sales_soup.find("table") # get the table on the webpage
rows = table.find_all("tr") # get all the rows in the table

# create a list of dicts which hold item data
items = scrape_data(rows)

# create the excel workbook
excel_workbook = openpyxl.Workbook()
excel_sheet = excel_workbook.active

format_excel(excel_sheet) # perform the required excel formatting

excel_sheet = insert_excel_data(items, excel_sheet) # insert the data into the excel sheet

excel_workbook.save("files/sales_data.xlsx") # save the excel workbook

# create a new spreadsheet
# google_workbook = ezsheets.createSpreadsheet("Office Supplies")

# use the spreadsheet created in the previous step
google_workbook = ezsheets.Spreadsheet('1qZ25oM4gyEChNvGikHq_L3S_o74JGVwppWQresExmTo')
google_sheet = google_workbook[0]

rows = insert_google_data(items, google_sheet) # insert the data into the google sheet

google_sheet.updateRows(rows) # update the google sheet with the new data