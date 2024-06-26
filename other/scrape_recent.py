import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL to scrape
url = "https://www.offers.com/deals"

# Data list to hold all extracted data
coupons_data = []

# Function to set up the WebDriver
def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver

# Save data to a JSON file function
def save_data(coupons_data):
    with open("recent_coupon_data.json", "w", encoding='utf-8') as file:
        json.dump(coupons_data, file, indent=4)
    print("Data has been saved successfully to 'recent_coupon_data.json'.")

# Process each deal
for deal_index in range(5):  # Adjust as necessary for number of deals
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    try:
        # Wait and click the deal at index deal_index
        deals = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-offer-id]")))
        if deal_index < len(deals):
            deals[deal_index].click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])

            # Extract coupon code and related data
            coupon_code_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[starts-with(@x-data, 'couponCode')]")))
            x_data = coupon_code_element.get_attribute('x-data')
            coupon_code = x_data.split(',')[1].strip().replace("'", "").replace(")", "").strip()

            preceding_div = coupon_code_element.find_element(By.XPATH, "./preceding-sibling::div[1]")
            preceding_content = preceding_div.text

            following_anchor = coupon_code_element.find_element(By.XPATH, "following::a[1]")
            following_link = following_anchor.get_attribute('href')
            following_text = following_anchor.text

            preceding_anchor = coupon_code_element.find_element(By.XPATH, "preceding::a[1]")
            preceding_image_src = preceding_anchor.find_element(By.TAG_NAME, 'img').get_attribute('src')
            preceding_link = preceding_anchor.get_attribute('href')

            # Store data
            coupon_data = {
                "coupon_code": coupon_code,
                "preceding_text": preceding_content,
                "following_link": {"url": following_link, "text": following_text},
                "preceding_image": {"src": preceding_image_src, "link": preceding_link}
            }
            coupons_data.append(coupon_data)
        else:
            print(f"No deal found at index {deal_index}")

    finally:
        # Close all tabs and quit driver
        driver.quit()

# After all iterations are done, save the collected data
save_data(coupons_data)
