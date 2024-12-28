#hello
from selenium import webdriver
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

#Website
#https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/15/wo/pxeePiFI6OnmxPJCcJKzq0/2.5

#Class ID
#E88F01
course_code = "E88F01"

current_directory = os.getcwd()
chromedriver_path = os.path.join(current_directory, "chromedriver")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

#default page - enter email and password in .env
driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")



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







