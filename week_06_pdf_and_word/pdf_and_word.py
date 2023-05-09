import docx
from functions.my_functions import *

# load each file via functions
operations_data = load_word_data("text_files/operations.docx")
sales_data = load_excel_data("text_files/sales.xlsx")
marketing_data = load_pdf_data("text_files/marketing.pdf")
IT_data = load_html_data("text_files/IT.html")

doc = docx.Document()

# write each file to a page in order
write_text_page(doc, "Operations", operations_data)
write_table_page(doc, "Sales", sales_data)
write_text_page(doc, "Marketing", marketing_data)
write_text_page(doc, "IT", IT_data, True)

doc.save("text_files/ceo_report.docx")