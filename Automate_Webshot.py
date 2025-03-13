from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv



load_dotenv()
base_url = os.getenv("BASE_URL")
# Get and split the URLs and IDs from .env
amazon_urls = json.loads(os.getenv("AMAZON_URLS"))
amazon_ids = json.loads(os.getenv("AMAZON_IDS"))

def scroll_down(driver):
    """
    Scroll down the page from the current position dynamically.
    
    :param driver: The Selenium WebDriver instance.
    :param pixels: The number of pixels to scroll down on each iteration (default: 1000).
    :param delay: The delay (in seconds) between scroll actions (default: 1.0).
    """
    try:
            total_height = driver.execute_script("return document.body.scrollHeight")
            current_position = 0
            print(total_height)
            while current_position < total_height:
                # Scroll by 1000 pixels at a time
                
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(1)  # Small delay between scrolls
                # Update the current height dynamically (useful for infinite scroll pages)
                current_position += 1000
                total_height = driver.execute_script("return document.body.scrollHeight")
            
    except Exception as e:
        print(f"An error occurred while scrolling: {e}")



def take_webshot(id):
    # move_mouse_and_click(3768,102)
    # move_mouse_and_click(3640, 332)
    # type_text(id)
    # move_mouse_and_click(3567, 462)
    # time.sleep(100)
    # move_mouse_and_click(3768,102)

    move_mouse_and_click(1849,91)
    move_mouse_and_click(1713, 325)
    type_text(id)
    move_mouse_and_click(1631, 467)
    time.sleep(20)
    move_mouse_and_click(1849,91)

def open_and_scroll(urls, ids, url):
    for url, product_id in zip(urls, ids):
        try:
            # Open the URL
            driver.get(url)
            
            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
          
            
            # Get the initial total height of the page
            scroll_down(driver)
            if "boulanger" in url:
                # Wait until the summary element is present
                summary_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "Description"))
                )

                # Click the summary element
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", summary_element)
                driver.execute_script("arguments[0].click();", summary_element)
                scroll_down(driver)
                time.sleep(5)
                voir_plus_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "bl-button.read-more__btn"))
                )
                # Click the button
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", voir_plus_button)
                driver.execute_script("arguments[0].click();", voir_plus_button)
            if "bestbuy" in url:
                from_manufacturer_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "fromTheManufacturer"))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", from_manufacturer_button)
                driver.execute_script("arguments[0].click();", from_manufacturer_button)
                time.sleep(10)
                scroll_down(driver)
                    # Define the specific video URL to look for
                # Define the specific video URL to look for
                video_urls = [
                    "https://cdn.cs.1worldsync.com/syndication/mediaserverredirect/f45534badd7fe56878033a6d14e02a63/original.mp4",
                    "https://cdn.cs.1worldsync.com/syndication/mediaserverredirect/b267c152a97864e67d7cb247a1d0da03/original.mp4",
                    "https://cdn.cs.1worldsync.com/syndication/mediaserverredirect/75a46810a4b26e9fee9977e6b56c64be/original.mp4",
                    "https://cdn.cs.1worldsync.com/syndication/mediaserverredirect/135475f7f26418e87a30baffec7a78f7/original.mp4"
                        ]

                # Iterate through the video URLs
                for specific_video_url in video_urls:
                    try:
                        # Locate the div containing the video by 'data-video-url'
                        video_container = driver.find_element(By.XPATH, f"//div[@data-video-url='{specific_video_url}']")
                        if video_container:
                            print(f"Video found with URL: {specific_video_url}")

                            # Focus on the video container
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", video_container)
                            print("Focused on video container.")
                            time.sleep(5)

                            # Locate the <video> tag within the container
                            video_element = video_container.find_element(By.TAG_NAME, "video")

                            # Play the video using JavaScript
                            driver.execute_script("arguments[0].play();", video_element)
                            print("Video started playing.")

                            # Add a short delay to let the video play for a few seconds
                            time.sleep(10)

                            # Skip to 12 seconds using JavaScript
                            driver.execute_script("arguments[0].currentTime = 12;", video_element)
                            print("Skipped to 12 seconds.")

                            # Pause the video at 12 seconds
                            driver.execute_script("arguments[0].pause();", video_element)
                            print("Video paused at 12 seconds.")

                            # Break the loop after finding and interacting with the first matching video
                            break
                    except Exception as e:
                        print(f"Video with URL {specific_video_url} not found: {str(e)}")
                else:
                    print("No matching videos found.")
        
            # Scroll all the way back up
            driver.execute_script("window.scrollTo(0, 0);")
            
            # Capture a screenshot
            take_webshot(product_id)
            
            # Log the progress
            print(f"Successfully processed URL: {url} with ID: {product_id}")
            time.sleep(2)  # Delay before processing the next URL
            
        except Exception as e:
            print(f"Error processing URL: {url} with ID: {product_id}. Error: {e}")


def type_text(text):
    subprocess.run(["xdotool", "type", str(text)])
def move_mouse_and_click(x, y):
    # Move mouse to (x, y) coordinates
    subprocess.run(["xdotool", "mousemove", str(x), str(y)])
    
    # Wait for a brief moment to ensure the mouse has moved
    time.sleep(0.5)
    
    # Perform a mouse click (left-click by default)
    subprocess.run(["xdotool", "click", "1"])
    time.sleep(2)
# Function to open URLs in pairs

zip_codes = {
    "www.amazon.ca": "K1A0A0",
    "www.amazon.co.uk": "EC1A1HQ",
    "www.amazon.com": "10001",
    "www.amazon.de": "10115",
    "www.amazon.es": "28015",
    "www.amazon.fr": "75001",
    "www.amazon.it": "00042",
}

extension_path = "/home/czarsosa/general_webshotter_service_reloaded_v4-1.1.24.xpi"
# Set up the Firefox WebDriver
options = webdriver.FirefoxOptions()
options.headless = False
options.set_preference('profile','/home/czarsosa/.mozilla/firefox/9ltc8ysk.default-release')
# Set preferences to force private mode in Firefox

service = Service('/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=options)
driver.install_addon(extension_path)
driver.maximize_window()

# Open the desired Amazon website
url = base_url
driver.get(url)
time.sleep(5)

# Get the domain from the URL
domain = driver.current_url.split("//")[1].split("/")[0]
# Get the corresponding ZIP code
if "bestbuy" in url:
    dialog = driver.find_element(By.ID, "onetrust-close-btn-container")
        # Click the button
    dialog.click()
    print("Accept button clicked.")
    time.sleep(2)
if "amazon" in url:
    try:
        # Locate the button by ID
        accept_button = driver.find_element(By.ID, "sp-cc-accept")
        # Click the button
        accept_button.click()
        print("Accept button clicked.")
        time.sleep(2)
    except NoSuchElementException:
        print("button does not exist.")
    if  "amazon.ca" in url or "amazon.es" in url or "amazon.fr" in url or "amazon.it" in url:
        # move_mouse_and_click(2129, 142)
        move_mouse_and_click(203, 138)
        time.sleep(3)
    else:
        location_button = driver.find_element(By.CSS_SELECTOR, "input[data-action-type='SELECT_LOCATION'].a-button-input")
        location_button.click()
        time.sleep(5)

    zip_code = zip_codes.get(domain)
    if not zip_code:
        print(f"No ZIP code available for the domain: {domain}")
        driver.quit()
        exit()
    
    zip_code_input = driver.find_element(By.XPATH, "//*[contains(@id, 'GLUXZipUpdateInput')]")
    driver.execute_script("arguments[0].scrollIntoView();", zip_code_input)
    ActionChains(driver).move_to_element(zip_code_input).click().perform()
    print("ZIPPPPPPP",zip_code)
    zip_code_input.send_keys(str(zip_code))

    # Find the "Apply" button and click it
    apply_button = driver.find_element(By.ID, "GLUXZipUpdate")
    time.sleep(2)
    apply_button.click()
    time.sleep(4)
if "worten" in url:
    try:
        # Wait for the captcha frame to load
        time.sleep(5)  # Adjust based on captcha loading time

        # Switch to the iframe if captcha is inside one
        captcha_iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'captcha')]")
        driver.switch_to.frame(captcha_iframe)

        # Find the captcha checkbox
        captcha_checkbox = driver.find_element(By.ID, "cf-chl-widget-et2t4_response")  # Adjust ID
        ActionChains(driver).move_to_element(captcha_checkbox).click().perform()

        print("Captcha clicked.")
        
    except Exception as e:
        print(f"Error interacting with captcha: {e}")

if "notebooksbilliger" in url:
    move_mouse_and_click(3073,791)
if "boulanger" in url:
        accept_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "popin_tc_privacy_button"))
                )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", accept_button)
        driver.execute_script("arguments[0].click();", accept_button)

# #EXTERNAL SCREEN
# move_mouse_and_click(3771,99)
# move_mouse_and_click(3761,195)
# move_mouse_and_click(3673,235)

# #LAPTOP SCREEN
move_mouse_and_click(1857,91)
move_mouse_and_click(1844,175)
move_mouse_and_click(1700,214)
time.sleep(10)
open_and_scroll(amazon_urls,amazon_ids,url)
# # Optional: Wait or interact further
print('Done webshots~')

# Close the browser
driver.quit()
