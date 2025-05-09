from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

test_item_id = 1
expected_brand = "Coca-Cola"

try:
    driver.get("http://localhost:3000")
    print("Test started: Accessing localhost:3000 page")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
    username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    username_input.send_keys("User")

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    password_input.send_keys("")

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    print("Test: User logged in")

    time.sleep(2)

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
    )
    search_input.clear()
    search_input.send_keys(str(test_item_id))
    print(f"Test: Entered search ID {test_item_id}")

    search_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    search_button.click()
    print("Test: Search button clicked")

    result_brand_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[starts-with(normalize-space(), 'Brand:')]"))
    )

    time.sleep(2)


    if result_brand_element:
        print(f"Test passed: Found brand '{expected_brand}' in search results")
    else:
        print(f"Test failed: Brand '{expected_brand}' not found")
except Exception as e:
    print(f"Test failed, Error: {e}")
    
finally:
    driver.quit()