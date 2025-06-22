from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
import json


def parse_course(course_url):
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(course_url)

    # Wait for JS-rendered content
    time.sleep(3)

    # Get page source
    rendered_html = driver.page_source
    driver.quit()

    # Extract course code from URL
    course_code = course_url.strip("/").split("/")[-1].replace(".html", "")

    # Save raw HTML
    os.makedirs("rendered_pages", exist_ok=True)
    html_path = f"rendered_pages/{course_code}_full_page.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        print(f"✅ Saved full page to '{html_path}'")

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(rendered_html, "html.parser")

    # Extract course title and code
    course_code_text = soup.select_one("#content-title")
    course_title_text = soup.select_one("#course-title")

    data = {
        "url": course_url,
        "course_code": (
            course_code_text.get_text(strip=True)
            if course_code_text
            else course_code.upper()
        ),
        "course_title": (
            course_title_text.get_text(strip=True)
            if course_title_text
            else "No title found"
        ),
    }

    # Section mappings
    sections = {
        "overview": "#content-section-overview",
        "outline": "#content-section-outline",
        "learning_outcomes": "#content-section-outcomes",
        "evaluation": "#content-section-evaluation",
        "materials": "#content-section-materials",
        "challenge": "#content-section-challenge",
        "important_links": "#content-section-links",
    }

    for key, selector in sections.items():
        section = soup.select_one(selector)
        if section:
            text = section.get_text(separator="\n", strip=True)
            data[key] = text

    # Save structured data to JSON
    os.makedirs("parsed_courses", exist_ok=True)
    json_path = f"parsed_courses/{course_code}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved structured data to '{json_path}'")

    return data
