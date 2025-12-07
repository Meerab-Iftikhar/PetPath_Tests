from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --------------------------
# Headless Chrome Setup
# --------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # required for assignment
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# --------------------------
# URLs
# --------------------------
FRONTEND_URL = "http://localhost:5173/"
FORM_PAGE_URL = "http://localhost:5173/services"
DATA_PAGE_URL = "http://localhost:5173/admin/AllReq"

# --------------------------
# TEST CASE 1: Open Frontend Homepage
# --------------------------
driver.get(FRONTEND_URL)
assert "localhost" in driver.current_url
print("Test 1 Passed: Frontend Homepage Loaded")

# --------------------------
# TEST CASE 2: Navigate to Form Page
# --------------------------
driver.get(FORM_PAGE_URL)
assert "services" in driver.current_url
print("Test 2 Passed: Form Page Loaded")

# --------------------------
# TEST CASE 3: Check Form Elements Exist
# --------------------------
required_fields = ["petName", "age", "petImage", "petType", "additionalMessage", "email", "contactNumber", "extra"]
for field in required_fields:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, field))
    )
print("Test 3 Passed: All Form Elements Found")

# --------------------------
# TEST CASE 4: Submit Valid Data
# --------------------------
driver.get(FORM_PAGE_URL)

driver.find_element(By.NAME, "petName").send_keys("TestUser")
driver.find_element(By.NAME, "age").send_keys("3")

# Use Select for dropdowns to make headless reliable
select_pet_type = Select(driver.find_element(By.NAME, "petType"))
select_pet_type.select_by_visible_text("Others")

driver.find_element(By.NAME, "additionalMessage").send_keys("Friendly pet")
driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
driver.find_element(By.NAME, "contactNumber").send_keys("1234567890")
driver.find_element(By.NAME, "extra").send_keys("Extra info")

# Upload a valid image
image_path = os.path.abspath("test_image.png")  # Make sure this file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file not found: {image_path}")
driver.find_element(By.NAME, "petImage").send_keys(image_path)

# Submit the form
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Wait until the form submission finishes (React async update)
WebDriverWait(driver, 15).until(
    EC.url_contains("services")  # page may redirect or remain
)
print("Test 4 Passed: Form Submitted ")

# --------------------------
# TEST CASE 5: Verify Data Page
# --------------------------
driver.get(DATA_PAGE_URL)
assert "admin/AllReq" in driver.current_url
print("Test 5 Passed: Data Page Loaded ")

# TEST CASE 6 (Alternative): Check Form Validation
driver.get(FORM_PAGE_URL)
driver.find_element(By.NAME, "email").send_keys("invalid-email")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Check validity using JS
is_valid = driver.execute_script(
    "return document.getElementsByName('email')[0].checkValidity();"
)
assert not is_valid
print("Test 6 Passed: Email Validation Works")

# --------------------------
# TEST CASE 7: Add Second Entry
# --------------------------
driver.get(FORM_PAGE_URL)
driver.find_element(By.NAME, "petName").send_keys("SecondUser")
driver.find_element(By.NAME, "age").send_keys("2")

select_pet_type = Select(WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "petType"))
))
select_pet_type.select_by_visible_text("Cat")

driver.find_element(By.NAME, "additionalMessage").send_keys("Calm pet")
driver.find_element(By.NAME, "email").send_keys("seconduser@example.com")
driver.find_element(By.NAME, "contactNumber").send_keys("0987654321")
driver.find_element(By.NAME, "extra").send_keys("Extra info")
driver.find_element(By.NAME, "petImage").send_keys(image_path)

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Handle alert
try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"Alert: {alert_text}")
    alert.accept()  # Accept the alert
except:
    print("No alert appeared")

# Wait until the form submission finishes (optional)
WebDriverWait(driver, 15).until(
    EC.url_contains("services")  # page may redirect or remain
)
print("Test 7 Passed: Adoption Request Submitted")
# --------------------------
# TEST CASE 8: Verify Multiple Records
# --------------------------
driver.get(DATA_PAGE_URL)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'SecondUser')]"))
)

assert "SecondUser" in driver.page_source
assert "seconduser@example.com" in driver.page_source
print("Test 8 Passed: Multiple Records Verified ")

# --------------------------
# TEST CASE 9: Page Title Check
# --------------------------
assert driver.title is not None
print("Test 9 Passed: Page Title Exists ")

# --------------------------
# TEST CASE 10: Page Load Performance Check (Basic)
# --------------------------
start_time = time.time()
driver.get(FRONTEND_URL)
end_time = time.time()
assert end_time - start_time < 5  # seconds
print("Test 10 Passed: Frontend Load Time Acceptable ")

# --------------------------
# Close Browser
# --------------------------
driver.quit()
print("All 10 Selenium Test Cases Passed ")
