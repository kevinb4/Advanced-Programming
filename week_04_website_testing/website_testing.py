import shutil
from classes.browser import Browser

browser = Browser("https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week04/WI20-website-testing-sites/assignment/index.php")

# define elements
first_name = browser.find_id("firstName")
last_name = browser.find_id("lastName")
email = browser.find_id("emailAddress")
phone = browser.find_id("phoneNumber")
submit = browser.find_id("my_submit")

# test everything with empty values
browser.save_screenshot("images/empty.png")
submit.click()

errors = ["First name is required", "Last name is required", "Phone number is required"]
check = browser.check_errors(errors)

# rename screenshot if check passed
if check:
    shutil.move("images/empty.png", "images/passed_empty.png")

# test too short of a first name
browser.test_invalid_element(first_name, submit, "A", "short_first_name", ["length of the First name"])

# test too long of a first name
browser.test_invalid_element(first_name, submit, "A" * 11, "long_first_name", ["length of the First name"])

# test too short of a last name
browser.test_invalid_element(last_name, submit, "B", "short_last_name", ["length of the Last name"])

# test too long of a last name
browser.test_invalid_element(last_name, submit, "B" * 16, "long_last_name", ["length of the Last name"])

# test incorrect email
browser.test_invalid_element(email, submit, "test@company", "incorrect_email", ["email address is in an incorrect format"])

# test too short of a phone number
browser.test_invalid_element(phone, submit, "1", "short_phone", ["phone number is an incorrect format"])

# test too long of a phone number
browser.test_invalid_element(phone, submit, "1" * 11, "long_phone", ["phone number is an incorrect format"])

# test valid first name
browser.test_valid_element(first_name, submit, "John", "valid_first_name")

# test valid last name
browser.test_valid_element(last_name, submit, "Smith", "valid_last_name")

# test valid email
browser.test_valid_element(email, submit, "test@company.com", "valid_email")

# test valid phone number
browser.test_valid_element(phone, submit, "1234567890", "valid_phone")

# test valid phone with dashes
browser.test_valid_element(phone, submit, "123-456-7890", "valid_phone_dashes")

# test valid phone with dots
browser.test_valid_element(phone, submit, "123.456.7890", "valid_phone_dots")

# test valid phone with spaces
browser.test_valid_element(phone, submit, "123 456 7890", "valid_phone_spaces")

# test valid submission
first_name.send_keys("John")
last_name.send_keys("Smith")
email.send_keys("test@company.com")
phone.send_keys("1234567890")
browser.save_screenshot("images/valid_submission.png")
submit.click()

elements = browser.find_tag("h1")

for element in elements:
    if element.text == "Thank You!":
        shutil.move("images/valid_submission.png", "images/passed_valid_submission.png")
        break

browser.browser.close()