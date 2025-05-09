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

purchase_quantity = 1
user_type = "user"
admin_flag_false = False
admin_flag_true = True
test_item_brand = "Coca-Cola"

item_id = ''
item_brand = ''
item_title = ''
item_price = ''
previous_quantity =''

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

    response = requests.get("http://localhost:8000/items/all-items")
    response.raise_for_status()
    items = response.json()

    item_to_purchase = next((item for item in items if item["brand"] == test_item_brand), None)

    if not item_to_purchase:
        raise Exception(f"Item '{test_item_brand}' not found in DB")

    item_id = item_to_purchase["id"]
    item_brand = item_to_purchase["brand"]
    item_title = item_to_purchase["title"]
    item_price = item_to_purchase["price"]
    previous_quantity = item_to_purchase["quantity"]
    print(f"Item found: ID {item_id}, Current Quantity {previous_quantity}")

    purchase_payload = {
        "id": item_id,
        "quantity": purchase_quantity
    }
    purchase_response = requests.put(
        f"http://localhost:8000/users/purchase/{user_type}?admin={str(admin_flag_false).lower()}",
        json=purchase_payload
    )
    purchase_response.raise_for_status()

    result_message = purchase_response.json().get("message", "")
    print(f"Test passed: Purchase response: {result_message}")

    time.sleep(1)
    check_response = requests.get("http://localhost:8000/items/all-items")
    check_response.raise_for_status()
    updated_items = check_response.json()
    updated_item = next((item for item in updated_items if item["id"] == item_id), None)

    if updated_item and updated_item["quantity"] == previous_quantity - purchase_quantity:
        print(f"Test passed: Item quantity updated correctly to {updated_item['quantity']}")
    else:
        print("Test failed: Quantity not updated as expected")

except Exception as e:
    print(f"Test failed, Error: {e}")

finally:
    driver.quit()

    try:
        restore_payload = {
            "id": item_id,
            "title": item_title,
            "brand": item_brand,
            "price": item_price,
            "quantity": previous_quantity
        }
        restore_response = requests.put(
            f"http://localhost:8000/items/update-item/{item_id}",
            json=restore_payload
        )
        restore_response.raise_for_status()
        print(f"Cleanup: Item quantity restored")
    except Exception as e:
        print(f"Cleanup failed: {e}")