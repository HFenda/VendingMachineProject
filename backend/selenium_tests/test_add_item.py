from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("http://localhost:3000")
    print("Test started: Accessing localhost:3000 page")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
    username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    username_input.send_keys("Admin")

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    password_input.send_keys("admin123")

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    print("Test: Admin logged in")

    time.sleep(2)

    print("Test: Accessing the Add Item page")

    item_name_input = driver.find_element(By.CSS_SELECTOR, 'input[id="title"]')
    item_name_input.clear()
    item_name_input.send_keys("New Item")

    item_brand_input = driver.find_element(By.CSS_SELECTOR, 'input[id="brand"]')
    item_brand_input.clear()
    item_brand_input.send_keys("New Brand")

    item_price_input = driver.find_element(By.CSS_SELECTOR, 'input[id="price"]')
    item_price_input.clear()
    item_price_input.send_keys("3")

    item_quantity_input = driver.find_element(By.CSS_SELECTOR, 'input[id="quantity"]')
    item_quantity_input.clear()
    item_quantity_input.send_keys("15")

    time.sleep(2)

    add_item_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#add_item')))
    add_item_button.click()

    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Item added successfully!')]"))
    )
    print("Test passed: Item successfully added")

    item_name_displayed = driver.find_element(By.CSS_SELECTOR, 'input[id="title"]')
    if item_name_displayed == "New Item":
        print("Test passed: Item appears in the item list")
    else:
        print("Test failed: Item does not appear in the item list")

    print("Test finished: Add item attempt completed")

except Exception as e:
    print(f"Test failed, Error: {e}")

finally:
    driver.quit()
