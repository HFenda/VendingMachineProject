from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service()

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("http://localhost:3000")
    time.sleep(2)

    print("Test started: Accessing localhost:3000 page")

    username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    username_input.send_keys("Admin")

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    password_input.send_keys("admin123")

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    time.sleep(3)

    if "admin" in driver.current_url:
        print("Test passed: Admin logged in successfully.")
    else:
        print("Test failed: Admin login failed.")

    driver.get("http://localhost:3000")
    time.sleep(2)

    username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    username_input.send_keys("User")

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    password_input.send_keys("")

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    time.sleep(3)

    if "user" in driver.current_url:
        print("Test passed: User logged in successfully.")
    else:
        print("Test failed: User login failed.")

    print("Test finished: Login attempts were made for Admin and User.")

except Exception as e:
    print(f"Test failed, Error: {e}")
    
finally:
    driver.quit()
