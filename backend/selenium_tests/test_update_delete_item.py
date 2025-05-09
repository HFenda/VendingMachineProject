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

item_id=""
target_item_title = "New Item"
updated_title = "New Brand"
updated_price = 4
updated_quantity = 20

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

    response = requests.get("http://localhost:8000/items/all-items")
    response.raise_for_status()
    items = response.json()

    item_to_update = next((item for item in items if item["title"] == target_item_title), None)
    if not item_to_update:
        raise Exception(f"Test failed: Item '{target_item_title}' not found.")

    item_id = item_to_update["id"]
    print(f"Test: Found item with ID {item_id}")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.p-4.border.rounded-xl.shadow-md.bg-white'))
    )

    cards = driver.find_elements(By.CSS_SELECTOR, 'div.p-4.border.rounded-xl.shadow-md.bg-white')
    print(f"Found {len(cards)} cards")

    found = False
    for card in cards:
        title_element = card.find_element(By.CSS_SELECTOR, 'h2.text-xl')
        if title_element.text == target_item_title:
            print(f"Found matching card for item '{target_item_title}'")
            edit_button = WebDriverWait(card, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#edit_item'))
            )
            edit_button.click()
            found = True
            break

    if not found:
        raise Exception(f"Could not find card containing item with title '{target_item_title}'")


    updated_title_input = driver.find_element(By.CSS_SELECTOR, 'input[id="title"]')
    updated_title_input.clear()
    updated_title_input.send_keys(f'{target_item_title}')
    
    updated_brand_input = driver.find_element(By.CSS_SELECTOR, 'input[id="brand"]')
    updated_brand_input.clear()
    updated_brand_input.send_keys(item_to_update["brand"])

    updated_price_input = driver.find_element(By.CSS_SELECTOR, 'input[id="price"]')
    updated_price_input.clear()
    updated_price_input.send_keys(str(updated_price))

    updated_quantity_input = driver.find_element(By.CSS_SELECTOR, 'input[id="quantity"]')
    updated_quantity_input.clear()
    updated_quantity_input.send_keys(str(updated_quantity))

    time.sleep(2)

    update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#add_item')))
    time.sleep(2)
    update_button.click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Item updated successfully!')]"))
    )
    print("Test passed: Item updated successfully!")

    time.sleep(5)

    try:
        response = requests.get("http://localhost:8000/items/all-items")
        response.raise_for_status()
        items = response.json()

        item_to_delete = next((item for item in items if item["title"] == "New Item"), None)

        if item_to_delete:
            delete_response = requests.delete(f"http://localhost:8000/items/delete-item/{item_to_delete["id"]}")
            delete_response.raise_for_status()
            print(f"Cleanup: Item with ID {item_id} deleted successfully.({item_to_delete["title"]})")
        else:
            print("Cleanup: Item not found in database.")

    except Exception as e:
        print(f"Cleanup failed: {e}")

except Exception as e:
    print(f"Test failed, Error: {e}")

finally:
    driver.quit()
