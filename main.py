import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

TINDOG_URL = os.getenv("TINDOG_URL") # URL of the Tindog website

chrome_options = webdriver.ChromeOptions() # Create a new option object
chrome_options.add_experimental_option("detach", True) # Attach the driver to the background
user_data_dir = os.path.join(os.getcwd(), "chrome_profile") # Set the user data directory
chrome_options.add_argument(f"--user-data-dir={user_data_dir}") # Add the user data directory argument

driver = webdriver.Chrome(options=chrome_options) # Instantiate the driver
driver.get(TINDOG_URL) # Navigate to the GYM_URL
wait = WebDriverWait(driver, 5) # Create a new wait object

def login_automatically():
    """
    Login to the gym automatically
    """
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-tindog-login"))) # Wait for the login button to appear
    login_btn.click() # Click the login button

    login_facebark_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-facebark"))) # Wait for the login button to appear
    login_facebark_btn.click() # Click the login button

    base_window = driver.window_handles[0] # Get the current window handle
    facebark_window = driver.window_handles[1] # Get the second window handle
    driver.switch_to.window(facebark_window) # Switch to the second window

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email"))) # Wait for the email input field to appear
    email_input.clear() # Clear the email input field
    email_input.send_keys(os.getenv("TINDOG_EMAIL")) # Enter the email address from the .env file

    password_input = wait.until(EC.presence_of_element_located((By.ID, "pass"))) # Wait for the password input field to appear
    password_input.clear() # Clear the password input field
    password_input.send_keys(os.getenv("TINDOG_PASSWORD")) # Enter the password from the .env file

    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Log In']"))) # Wait for the Submit button to appear
    submit_btn.click() # Click the Submit button

    driver.switch_to.window(base_window) # Switch back to the first window

    # dismiss all requests
    allow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))) # Wait for the "Allow" button to appear
    allow_btn.click() # Click the "Allow" button

    not_interested_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary"))) # Wait for the "Not interested" button to appear
    not_interested_btn.click()  # Click the "Not interested" button

    cookies_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))) # Wait for the "I accept" button to appear
    cookies_btn.click() # Click the "I accept" button

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "main.tindog-swipe-container"))) # Wait for the main element to appear

    return "OK"
def like_dog():
    for i in range(20): # Like the dog 20 times
        try: # Try to like the dog
            like_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-like")))  # Wait for the like button to appear
            like_btn.click()  # Click the like button

        except ElementClickInterceptedException: # If the like button is not clickable, try again
            try: # Try to click the like button again
                close_popup = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".match-popup a"))) # Wait for the close popup button to appear
                close_popup.click() # Click the close popup button
            except TimeoutException: # If the close popup button is not clickable, try again
                pass # Do nothing

        except NoSuchElementException: # If the like button is not found, try again
            try: # Try to click the like button again
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-like"))) # Wait for the like button to appear
            except TimeoutException: # If the like button is not clickable, try again
                pass # Do nothing
def retry(func, retries=7, description=None):
    """
    Retry a function if it fails
    :param func: a function to retry
    :param retries: retry count
    :param description: description of the function
    :return: function result
    """
    for attempt in range(1, retries + 1): # Retry up to retries times
        try: # Try to execute the function
            print(f"Attempt {attempt}/{retries} → {description}") # Print the attempt number
            return func() # Return the function result

        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, Exception) as e:
            print(f"Failed attempt {attempt}: {e}") # Print the failure message
            time.sleep(1) # Wait for 1 second before retrying

    raise Exception(f"❌ All retries failed for: {description}") # If all retries fail, raise an exception

retry(login_automatically, description="Login") # Call the login_automatically function with retries
retry(like_dog, description="Like a dog") # Call the like_dog function with retries