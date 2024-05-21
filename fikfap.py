from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")

# Create a new instance of the Chrome driver
service = Service('/opt/homebrew/bin/chromedriver')  # specify the path to chromedriver if it's not in PATH
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to extract video links
def get_video_links(driver):
    video_links = set()
    elements = driver.find_elements(By.TAG_NAME, 'video')
    print(elements)
    for element in elements:
        source = element.get_attribute('src')
        print(source)
        # if source and '.mp4' in source:
        video_links.add(source)
    return video_links

# Open the website
driver.get('https://fikfap.com')  # replace with the target website URL

while True:
    try:

        # Wait for the page to load
        time.sleep(1)

        # write html to file
        with open('fikfap.html', 'w') as file:
            file.write(driver.page_source)

        # Get video links
        video_links = get_video_links(driver)

        # Convert the set to a list and sort it
        video_links = sorted(list(video_links))

        # Load old video links from the file if it exists
        try:
            with open('data.json', 'r') as file:
                old_videos = json.load(file)
        except FileNotFoundError:
            old_videos = []

        # Combine old and new video links, remove duplicates
        all_video_links = list(set(old_videos + video_links))

        # Save the combined list back to the file
        # with open('data.json', 'w') as file:
        #     json.dump(all_video_links, file, indent=4)

        print("Video links have been saved to data.json")

        # Press the key down to scroll
        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_DOWN)

        # Wait before next iteration
        time.sleep(2)  # Adjust the sleep time as needed

    except Exception as e:
        print(f"An error occurred: {e}")


