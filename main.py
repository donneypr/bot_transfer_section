#hello
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Load environment variables
load_dotenv()
myusername = os.getenv("USERNAME")
mypassword = os.getenv("PASSWORD")

# Class ID
course_code = "E88F01"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking") 
chrome_options.add_argument("--disable-notifications")  
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")  

current_directory = os.getcwd()
chromedriver_path = os.path.join(current_directory, "chromedriver")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")

time.sleep(2)
username_input = driver.find_element(By.ID, "mli")
username_input.clear()
username_input.send_keys(myusername)

password_input = driver.find_element(By.NAME, "password")
password_input.clear()
password_input.send_keys(mypassword)

log_in = driver.find_element(By.NAME, "dologin")
log_in.click()

time.sleep(5)

print("Logged in successfully. Waiting for user action.")

wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
verification_code_element = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
)

print("Verification code content:", verification_code_element.text)

time.sleep(600)

# Quit the driver after completion
driver.quit()
