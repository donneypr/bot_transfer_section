#hello
from selenium import webdriver
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv


#loadenv files
load_dotenv()
myusername = os.getenv("USERNAME")
mypassword = os.getenv("PASSWORD")


driver = webdriver.Chrome()


#Class ID
course_code = "E88F01"

current_directory = os.getcwd()
chromedriver_path = os.path.join(current_directory, "chromedriver")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

#default page - enter email and password in .env
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

# time.sleep(1)

# otherwaysbutton = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[3]/div/button')
# otherwaysbutton.click()

# time.sleep(2)

# auth_method_icon = driver.find_element(By.CLASS_NAME, "auth-method-icon")
# auth_method_icon.click()


time.sleep(300)

#duo-page
#enter duo number
#click ID with id="trust-browser-button"
#click href="https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem"

#yorku rem page
#select right academic session
#click type="submit"

#main yorkurem page
#click title="Transfer a Course"
#input course ID into name="5.1.27.7.7"







