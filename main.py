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
mybypasscode = os.getenv("BYPASSCODE")

course_code = "E88F01" #classid
vsb = "https://schedulebuilder.yorku.ca/vsb/criteria.jsp?access=0&lang=en&tip=1&page=results&scratch=0&term=0&sort=none&filters=iiiiiiii&bbs=&ds=&cams=0_1_2_3_4_5_6&locs=any"
rem = "https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking") 
chrome_options.add_argument("--disable-notifications")  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  

current_directory = os.getcwd()
chromedriver_path = os.path.join(current_directory, "chromedriver")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(vsb)

time.sleep(2)

#need to modualarize by making this it's own function

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

wait = WebDriverWait(driver, 10)  
verification_code_element = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
)

print("Verification code content:", verification_code_element.text)

time.sleep(5)

wait = WebDriverWait(driver, 10)
other_options_button = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "other-options-link"))
)
other_options_button.click()

time.sleep(1)

try:
    bypass_code_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="test-id-bypass"]'))
    )
    bypass_code_link.click()
    print("Successfully clicked the bypass code link.")
except Exception as e:
    print(f"An error occurred: {e}")


wait = WebDriverWait(driver, 10)
bypass_code_input = wait.until(
    EC.visibility_of_element_located((By.ID, "passcode-input"))
)

# Enter the bypass code
bypass_code_input.send_keys(mybypasscode)
print("bypass code inputted")

try:
    verify_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="verify-button"]'))
    )
    verify_button.click()
    print("Successfully clicked the verify button.")
except Exception as e:
    print(f"An error occurred while clicking the verify button: {e}")

try:
    trust_browser_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "trust-browser-button"))
    )
    trust_browser_button.click()
    print("Successfully clicked the 'Trust Browser' button.")
except Exception as e:
    print(f"An error occurred while clicking the button: {e}")

time.sleep(10)

term_radio_button = driver.find_element(By.ID, "term_2024102119")
term_radio_button.click()

time.sleep(2)

course_input = driver.find_element(By.ID, "code_number")
course_input.clear()  
course_input.send_keys(course_code)

wait = WebDriverWait(driver, 10)  
add_course_button = wait.until(
    EC.element_to_be_clickable((By.ID, "addCourseButton"))
)

add_course_button.click()
print("Successfully clicked the 'Add Course' button.")

time.sleep(3)

try:
    warning_message_element = driver.find_element(By.XPATH, '//*[@id="requirements"]/div[3]/div[2]/div[5]/div/span')
    warning_text = warning_message_element.text.strip()
    if "All classes are full" in warning_text:
        print("The course is full.")
    elif not warning_text:
        print("Course is Available")
    else:
        print(f"Unexpected status: {warning_text}")
except Exception as e:
    print("The course is available (warningMessage element not found).")
    print(f"Error: {e}")

driver.save_screenshot('screenshot.png')

time.sleep(600)

driver.quit()
