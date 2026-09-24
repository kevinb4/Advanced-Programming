# Advanced Programming

A course focused on practical Python automation - scripting solutions to real-world tasks like file organization, data extraction, browser testing, document generation, database ETL, and scheduled monitoring jobs.

## Structure

<dl>
<dt><strong>Week 1: Regular Expressions</strong></dt>
<dd>A clipboard utility that reads copied text, uses regex to extract coordinates, dollar amounts, and credit card numbers, formats them into a table, and copies the result back to the clipboard.</dd>

<dt><strong>Week 2: Reading and Writing Files</strong></dt>
<dd>A file-copy utility that recursively copies files (including one level of subfolders) from a source directory to a destination, skipping files over 1GB and logging every action (copied, skipped, or failed) to a log file.</dd>

<dt><strong>Week 3: Organizing Files</strong></dt>
<dd>A log-processing pipeline that unzips a batch of access logs, scans each file with regex for suspicious patterns (directory traversal, SQL injection attempts, failed logins, etc.), extracts the offending IPs, renames matched files, discards files with no matches via the recycle bin, and re-zips the results.</dd>

<dt><strong>Week 4: Website Testing</strong></dt>
<dd>Automated browser testing with Selenium. A Browser class wraps ChromeDriver to fill out and submit a web form, check for validation error messages, and take screenshots of pass/fail states, covering both invalid inputs (short/long names, bad email, bad phone formats) and valid submissions.</dd>

<dt><strong>Week 5: Spreadsheets</strong></dt>
<dd>Web scraping combined with spreadsheet automation - scrapes a sales data table from a webpage with BeautifulSoup, writes it into a formatted Excel workbook with openpyxl, and pushes the same data into a Google Sheet using the ezsheets API.</dd>

<dt><strong>Week 6: PDF and Word</strong></dt>
<dd>A document-aggregation tool that pulls content from four different file types - a Word doc, an Excel sheet, a PDF, and an HTML file - and compiles them into a single formatted Word report (ceo_report.docx) with one page per source.</dd>

<dt><strong>Week 7: Database Automation</strong></dt>
<dd>A CLI ETL tool that imports address data from CSV, JSON, or XML into a MySQL staging table, then atomically swaps it in as the live table via a sequence of table renames wrapped in a transaction, so the production table is never left in a partial state.</dd>

<dt><strong>Week 8: Scheduling Tasks</strong></dt>
<dd>A script designed to run unattended via a task scheduler (Windows Task Scheduler/cron). It downloads exam data from a remote source, parses it, and fans it out concurrently using threads to Excel, Google Sheets, and a MySQL database.</dd>

<dt><strong>Week 9: System Monitoring</strong></dt>
<dd>A scheduled monitoring script (via psutil) that checks CPU, RAM, disk, and network error thresholds, sends an SMS alert through Twilio when something crosses a threshold, and emails a full system status report twice a day.</dd>

<dt><strong>Week 10: Manipulating Images</strong></dt>
<dd>A batch image-processing tool that scrapes employee headshots and info from a webpage, overlays each photo with a company logo watermark plus the employee's name and title using Pillow, and zips up the finished set of images.</dd>
</dl>

## Tech Stack
- Python 3
- Selenium/ChromeDriver
- BeautifulSoup
- openpyxl
- ezsheets (Google Sheets)
- python-docx
- PyPDF4
- psutil
- Twilio
- Pillow
- MySQL
