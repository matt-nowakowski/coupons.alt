import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome with Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# List of URLs and company names
urls = [
    {"url": "https://www.offers.com/stores/cos", "company": "COS"},
    {"url": "https://www.offers.com/stores/adidas", "company": "Adidas"},
    {"url": "https://www.offers.com/stores/kate-spade/", "company": "Kate Spade"},
    {"url": "https://www.offers.com/stores/gap/", "company": "Gap"}
]

# List to hold all coupon data
coupons_data = []

try:
    for entry in urls:
        driver.get(entry["url"])
        wait = WebDriverWait(driver, 10)

        # Wait and click the first deal
        first_deal = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-offer-id]")))
        first_deal.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])

        # Extract coupon code
        coupon_code_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[starts-with(@x-data, 'couponCode')]")))
        x_data = coupon_code_element.get_attribute('x-data')
        coupon_code = x_data.split(',')[1].strip().replace("'", "").replace(")", "").strip()

        # Get the preceding div's content
        preceding_div = coupon_code_element.find_element(By.XPATH, "./preceding-sibling::div[1]")
        preceding_content = preceding_div.text

        following_anchor = coupon_code_element.find_element(By.XPATH, "following::a[1]")
        following_link = following_anchor.get_attribute('href')
        following_text = following_anchor.text

        preceding_anchor = coupon_code_element.find_element(By.XPATH, "preceding::a[1]")
        preceding_image_src = preceding_anchor.find_element(By.TAG_NAME, 'img').get_attribute('src')
        preceding_link = preceding_anchor.get_attribute('href')


        # Store data
        coupons_data.append({
            "company": entry["company"],
            "coupon_code": coupon_code,
            "preceding_text": preceding_content,
            "following_link": {"url": following_link, "text": following_text},
            "preceding_image": {"src": preceding_image_src, "link": preceding_link}
        })

        # Close the current tab and switch back to the first tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()

# Save data to a JSON file
with open("fav_coupon_data.json", "w", encoding='utf-8') as file:
    json.dump(coupons_data, file, indent=4)

print("Data has been saved successfully to 'coupon_data.json'.")
