import requests
from bs4 import BeautifulSoup

def parse_course(course_url):
    # Fetch the course page content
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract course title
    title = soup.find("h1").text.strip() if soup.find("h1") else "No title found"

    # Grab the main content area
    main = soup.find("main")
    text = main.get_text(separator="\n") if main else ""

    # Try to extract Learning Outcomes by keyword
    learning_outcomes = []
    layout = ""
    topics = []

    # Very rough segmentation based on known text patterns
    for section in text.split("\n"):
        section = section.strip()
        if "Learning Outcomes" in section:
            learning_outcomes.append(section)
        elif "Topics Covered" in section or "Units" in section:
            topics.append(section)
        elif "Course Layout" in section or "Structure" in section:
            layout += section + "\n"

    return {
        "url": course_url,
        "title": title,
        "learning_outcomes": learning_outcomes,
        "topics": topics,
        "layout": layout.strip()
    }
