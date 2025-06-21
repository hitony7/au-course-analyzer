import requests
from bs4 import BeautifulSoup

def parse_course(course_url):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()
    learning_outcomes = [li.text.strip() for li in soup.select("ul.learning-outcomes li")]
    topics = [li.text.strip() for li in soup.select("ul.topics li")]
    layout = soup.find("div", class_="course-layout").text.strip()

    return {
        "url": course_url,
        "title": title,
        "learning_outcomes": learning_outcomes,
        "topics": topics,
        "layout": layout
    }