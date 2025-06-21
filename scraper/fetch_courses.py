import requests
from bs4 import BeautifulSoup

def fetch_course_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    course_links = []
    for a_tag in soup.select("a.course-link"):
        href = a_tag.get("href")
        if href:
            course_links.append(href)

    return course_links