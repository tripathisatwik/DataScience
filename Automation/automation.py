from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver_path = 'Automation/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

url = 'https://example.com/login'
driver.get(url)

time.sleep(2)

username_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

username_field.send_keys('your_username')
password_field.send_keys('your_password')

password_field.send_keys(Keys.RETURN)

time.sleep(2)

data_elements = driver.find_elements(By.CLASS_NAME, 'data-element-class')

for element in data_elements:
    print(element.text)

driver.quit()