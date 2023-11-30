"""
SIP Payment for NIC ASIA Bank via Selenium Automation
Author: Namit Adhikari
"""

import os
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

BASE_URL = os.getenv("SIP_PAYMENT_LOGIN_URL")
# SIP Payment Creds
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Payment Gateway Creds
ESEWA_USERNAME = os.getenv("ESEWA_USERNAME")
ESEWA_PASSWORD = os.getenv("ESEWA_PASSWORD")


class Actions(ActionChains):
    def send_keys_slowly(
            self, element: WebElement, text: str, delay: float = 0.08
    ) -> "Actions":
        """Send a text to an element one character at a time with a delay."""
        act = self.move_to_element(element).click()
        for character in text:
            act.send_keys(character)
            time.sleep(delay)
        return self

    def perform(self) -> None:
        super().perform()
        self.pause(0.4)


driver = webdriver.ChromiumEdge()
driver.get(BASE_URL)

action = Actions(driver)
action.pause(1.5)

wait = WebDriverWait(driver, 10)

# Fill out username, password and login
# action.move_to_element(
#     driver.find_element(By.XPATH, '//*[@id="login"]')
# ).click().send_keys(USERNAME).perform()
action.send_keys_slowly(
    driver.find_element(By.XPATH, '//*[@id="login"]'), USERNAME
).perform()

if not PASSWORD:
    PASSWORD = input("Please enter your NIC ASIA SIP Portal Password: ")

action.send_keys_slowly(
    driver.find_element(By.XPATH, '//*[@id="password"]'), PASSWORD
).perform()

action.move_to_element(
    driver.find_element(By.XPATH, '//*[@id="formContent"]/input[3]')
).click().perform()

# Open SIP Payment, and Proceed to Payment

# Expand SIP Menu
action.move_to_element(
    driver.find_element(By.XPATH, "/html/body/div[1]/aside/section/ul/li[5]/a")
).click().perform()

# Click on SIP Payment
action.move_to_element(
    driver.find_element(By.XPATH, '/html/body/div[1]/aside/section/ul/li[5]/ul/li[3]/a')
).click().perform()

# Load Payments
action.move_to_element(driver.find_element(By.ID, "LOAD")).click().perform()

# Select SIP Payment
payments = driver.find_elements(By.XPATH, "//input[@class='case']")
if not len(payments):
    print("No SIP Payments found.")
    driver.quit()
    sys.exit()

action.move_to_element(payments[0]).click().perform()

# Check whether Proceed can be clicked or not
elem = driver.find_element(By.ID, "btnProceed")

if not elem.is_enabled():
    elem = driver.find_element(By.ID, "DueDay-1")
    try:
        print(
            f"You can't Pay SIP at this time. "
            f"Please try again after {abs(int(elem.get_attribute('value')))} day(s)."
        )
    except ValueError:
        print("You can't Pay SIP at this time. Please try again after some days.")
    driver.quit()
    sys.exit()

amount = driver.find_element(
    By.XPATH, '/html/body/div[1]/div[4]/div[4]/div/div[2]/div[3]/div/div[2]/div/table/tbody/tr/td[5]'
).text
print(f"Amount to be paid: Rs. {amount}")

# Click on Proceed
action.move_to_element(elem).click().perform()

action.move_to_element(
    driver.find_elements(
        By.XPATH, '/html/body/div[1]/div[4]/div[5]/div/div/div[2]/table/tbody/tr/td[4]'
    )[0]
).click().perform()

input(f"Press Enter when you have topped up Rs. {amount} your ESEWA account...")

# Now, Pay Via Payment Gateway
action.send_keys_slowly(
    driver.find_element(By.XPATH,
                        '/html/body/div[2]/div/div[2]/div/div[2]/div/ng-include[1]/div/div/div/div[2]/form/div[1]/input'),
    ESEWA_USERNAME
).perform()

if not ESEWA_PASSWORD:
    ESEWA_PASSWORD = input("Please enter your ESEWA Password: ")

# Input Password
action.send_keys_slowly(
    driver.find_element(By.XPATH,
                        "/html/body/div[2]/div/div[2]/div/div[2]/div/ng-include[1]/div/div/div/div[2]/form/div[2]/input"),
    ESEWA_PASSWORD
).perform()

# Login
action.move_to_element(
    driver.find_element(By.XPATH,
                        "/html/body/div[2]/div/div[2]/div/div[2]/div/ng-include[1]/div/div/div/div[2]/form/div[3]/button[1]")
).click().perform()

# Ask for OTP
otp = input("Please input OTP here and Press Enter: ")

# Enter OTP
action.send_keys_slowly(
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[2]/div/input"), otp
).perform()

# Submit
action.move_to_element(
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[2]/button[1]')
).click().perform()

confirm_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[6]/button[1]")))
confirm_btn.click()

re_confirm_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/form/div[1]/button[1]")))
re_confirm_button.click()

action.move_to_element(
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[6]/div/div/div[2]/div/div/button[3]')
).click().perform()

print("Payment Successful!")

driver.quit()
