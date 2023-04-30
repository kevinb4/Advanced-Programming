import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Browser():
    """Defines the base class for the browser"""

    def __init__(self, url):
        """Initializes the Browser"""
        self.opt = Options()
        self.opt.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome("chromedriver.exe", options=self.opt)
        self.browser.get(url)

    def check_errors(self, errors):
        """Checks the error messages passed in"""
        error_message = self.get_alert()
        check_pass = True

        for error in errors:
            if error not in error_message:
                check_pass = False

        return check_pass
    
    def check_no_errors(self, name):
        """Checks for no errors"""
        error_message = self.get_alert()

        if name in error_message:
            return False
        else:
            return True

    def empty_fields(self, fields):
        """Empites all fields"""
        for field in fields:
            field.clear()

    def find_tag(self, tag):
        """Finds the element by tag"""
        return self.browser.find_elements(By.TAG_NAME, tag)

    def find_id(self, id):
        """Finds the element by id"""
        return self.browser.find_element(By.ID, id)
    
    def get_alert(self):
        """Gets the alert message"""
        alert = self.browser.switch_to.alert
        message = alert.text
        alert.accept()
        return message
    
    def save_screenshot(self, name):
        """Saves a screenshot"""
        self.browser.save_screenshot(name)

    def test_invalid_element(self, element, submit, test, image, errors):
        """Tests an invalid element"""
        element.send_keys(test)
        self.browser.save_screenshot(f"images/{image}.png")
        submit.click()

        if self.check_errors(errors):
            shutil.move(f"images/{image}.png", f"images/passed_{image}.png")

        element.clear()

    def test_valid_element(self, element, submit, test, image):
        """Tests a valid element"""
        element.send_keys(test)
        self.browser.save_screenshot(f"images/{image}.png")
        submit.click()

        if self.check_no_errors(test):
            shutil.move(f"images/{image}.png", f"images/passed_{image}.png")

        element.clear()