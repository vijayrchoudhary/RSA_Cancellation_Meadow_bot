import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Load credentials securely from GitHub Secrets
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
RSA_USERNAME = os.environ.get('RSA_USERNAME')
RSA_PASSWORD = os.environ.get('RSA_PASSWORD')

def send_telegram_message(message):
    """Sends a notification to your Telegram app."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_rsa_cancellations():
    print("Starting RSA check...")
    
    # 2. Configure Headless Chrome (Runs without a visible window on the server)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 3. Navigate to the RSA Portal
        driver.get("https://myroadsafety.rsa.ie/")
        wait = WebDriverWait(driver, 15)
        
        # --- UPDATE THESE IDs BASED ON THE LIVE RSA WEBSITE ---
        USERNAME_FIELD_ID = "username_element_id_here"
        PASSWORD_FIELD_ID = "password_element_id_here"
        LOGIN_BUTTON_ID = "login_button_id_here"
        # ------------------------------------------------------
        
        # 4. Log in
        username_field = wait.until(EC.presence_of_element_located((By.ID, USERNAME_FIELD_ID)))
        password_field = driver.find_element(By.ID, PASSWORD_FIELD_ID)
        login_button = driver.find_element(By.ID, LOGIN_BUTTON_ID)
        
        username_field.send_keys(RSA_USERNAME)
        password_field.send_keys(RSA_PASSWORD)
        login_button.click()
        
        time.sleep(5) # Wait for the dashboard to load
        
        # 5. Check for availability
        # (You may need to add code here to click to the specific test center page first)
        page_source = driver.page_source
        
        # Simple text check: If "No slots available" is missing, a slot might be open
        if "No slots available" not in page_source:
            send_telegram_message("🚨 DRIVING TEST SLOT AVAILABLE! Log in to RSA immediately: https://myroadsafety.rsa.ie/")
            print("Slot found! Message sent.")
        else:
            print("No slots available at this time.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_rsa_cancellations()
