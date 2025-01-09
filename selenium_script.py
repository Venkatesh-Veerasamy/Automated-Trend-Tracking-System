import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from datetime import datetime
import uuid

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["trends"]
collection = db["google_trends"]

def get_google_trends():
    # Chrome options for Selenium
    options = webdriver.ChromeOptions()
    
    # Specify the correct ChromeDriver path
    chrome_driver_path = r"F:\selenium\chrome-mac-arm64\chromedriver.exe"  # Update as needed
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to Google Trends homepage
        driver.get("https://trends.google.com/trends/trendingsearches/daily")
        time.sleep(5)  # Adjust as needed for page load time

        # Fetch trending topics
        trends = driver.find_elements(By.XPATH, "//div[@class='details-top']//a/span")
        top_trends = [trend.text for trend in trends[:5] if trend.text]

        # Save to MongoDB
        unique_id = str(uuid.uuid4())
        result = {
            "_id": unique_id,
            "trends": top_trends,
            "timestamp": datetime.now(),
        }
        collection.insert_one(result)
        return result

    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    data = get_google_trends()
    if data:
        print(json.dumps(data, indent=4, default=str))
