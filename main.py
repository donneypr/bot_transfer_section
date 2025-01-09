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
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support.ui import Select


# Load environment variables
load_dotenv()
myusername = os.getenv("USERNAME")
mypassword = os.getenv("PASSWORD")
mybypasscode = os.getenv("BYPASSCODE")

course_code = "W04U02" 
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


def open_broswer(driver, website):
    driver.get(website)

def login_and_bypass_verification(driver, website_url, myusername, mypassword, mybypasscode):
    try:
        # Navigate to the website
        driver.get(website_url)
        # Enter username
        wait = WebDriverWait(driver, 10)
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "mli"))
        )
        username_input.clear()
        username_input.send_keys(myusername)

        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(mypassword)

        # Click login button
        log_in = driver.find_element(By.NAME, "dologin")
        log_in.click()

        time.sleep(5)
        print("Logged in successfully. Waiting for user action.")

        # Wait for verification code element
        wait = WebDriverWait(driver, 10)
        verification_code_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
        )
        print("Verification code content:", verification_code_element.text)

        time.sleep(5)

        # Click 'Other Options'
        other_options_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "other-options-link"))
        )
        other_options_button.click()

        time.sleep(1)

        # Click 'Bypass Code' link
        try:
            bypass_code_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="test-id-bypass"]'))
            )
            bypass_code_link.click()
            print("Successfully clicked the bypass code link.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Enter bypass code
        bypass_code_input = wait.until(
            EC.visibility_of_element_located((By.ID, "passcode-input"))
        )
        bypass_code_input.send_keys(mybypasscode)
        print("Bypass code inputted.")

        # Click verify button
        try:
            verify_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="verify-button"]'))
            )
            verify_button.click()
            print("Successfully clicked the verify button.")
        except Exception as e:
            print(f"An error occurred while clicking the verify button: {e}")

        # Click 'Trust Browser' button
        try:
            trust_browser_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "trust-browser-button"))
            )
            trust_browser_button.click()
            print("Successfully clicked the 'Trust Browser' button.")
        except Exception as e:
            print(f"An error occurred while clicking the button: {e}")

        time.sleep(10)

    except Exception as e:
        print(f"An error occurred during the login and verification process: {e}")


def vsb_add_course(course_code):

    time.sleep(5)

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

def check_availability_with_refresh():
    while True:  # Keep checking until the course is available
        try:
            # Locate the warning message element
            warning_message_element = driver.find_element(By.XPATH, '//*[@id="requirements"]/div[3]/div[2]/div[5]/div/span')
            warning_text = warning_message_element.text.strip()

            if "All classes are full" in warning_text:
                print("The course is full. Refreshing the page in 30 seconds...")
                time.sleep(30)  # Wait before refreshing
                driver.refresh()  # Refresh the page
            elif not warning_text:
                print("Course is Available")
                return True  # Exit the loop and return True when available
            else:
                print(f"Unexpected status: {warning_text}")
                time.sleep(30)  # Wait before refreshing
                driver.refresh()  # Refresh the page
        except Exception as e:
            print("The course is available (warningMessage element not found).")
            print(f"Error: {e}")
            return True  # Assuming the course is available if no warning element is found



def transfer_section(course_code):
    dropdown = driver.find_element(By.NAME, "5.5.1.27.1.11.0")
    select = Select(dropdown)
    select.select_by_value("1") # fall/winter 2024-2025 option

    rembutton = driver.find_element(By.NAME, "5.5.1.27.1.13")  
    rembutton.click()

    time.sleep(1)

    transfer_course_button = driver.find_element(By.NAME, "5.1.27.1.27")
    transfer_course_button.click()

    input_element = driver.find_element(By.NAME, "5.1.27.7.7")  
    input_element.clear()  
    input_element.send_keys(course_code)

def rem_submit():
    add_rem_course = driver.find_element(By.NAME, "5.1.27.7.9")
    add_rem_course.click()

def enroll_into_course(course_code):

    dropdown = driver.find_element(By.NAME, "5.5.1.27.1.11.0")
    select = Select(dropdown)
    select.select_by_value("1") # fall/winter 2024-2025 option

    continuebutton = driver.find_element(By.NAME, "5.5.1.27.1.13")  
    continuebutton.click()

    time.sleep(1)
    
    addcourse = driver.find_element(By.NAME, "5.1.27.1.23")  
    addcourse.click()

    time.sleep(1)
    input_element = driver.find_element(By.NAME, "5.1.27.7.7")  
    input_element.clear()  
    input_element.send_keys(course_code)

    rem_submit()

    time.sleep(1)
    finalyes = driver.find_element(By.NAME, "5.1.27.11.11")
    finalyes.click()
                
login_and_bypass_verification(driver, vsb, myusername, mypassword, mybypasscode)
vsb_add_course(course_code)

#error might be because it's caching the old token in the broswer and tries to interact with the elements like it's trying to login for the first time
if (check_availability_with_refresh()):
    login_and_bypass_verification(driver,rem,myusername,mypassword,mybypasscode)
    enroll_into_course(course_code)
    driver.save_screenshot("screenshot.png")

#need to implement recurrent checking

time.sleep(600)

driver.quit()
