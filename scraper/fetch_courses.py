from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def fetch_course_metadata(base_url):
    # Set up headless browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Launch browser and navigate
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(base_url)
    time.sleep(5)  # Allow JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Find all course blocks
    course_data = []

    for div in soup.select('div[itemtype="http://schema.org/Course"]'):
        link = div.find("a", itemprop="url")
        code = div.find("strong", itemprop="courseCode")
        name = div.find("span", itemprop="name")

        if link and code and name:
            course_data.append({
                "course_code": code.text.strip().rstrip(":"),
                "course_name": name.text.strip(),
                "url": link.get("href")
            })

    # Save to file
    with open("au_courses.json", "w", encoding="utf-8") as f:
        json.dump(course_data, f, indent=2)
        print(f"✅ Saved {len(course_data)} course entries to 'au_courses.json'")

    return course_data
