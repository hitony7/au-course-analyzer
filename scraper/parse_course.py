import requests
from bs4 import BeautifulSoup

def parse_course(course_url):
    # Send a GET request to the course page
    response = requests.get(course_url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the course title from the <h1> tag
    title = soup.find("h1").text.strip()

    # Extract learning outcomes by selecting all <li> elements within a <ul> with class "learning-outcomes"
    learning_outcomes = [li.text.strip() for li in soup.select("ul.learning-outcomes li")]

    # Extract topics by selecting all <li> elements within a <ul> with class "topics"
    topics = [li.text.strip() for li in soup.select("ul.topics li")]

    # Extract course layout from a <div> with class "course-layout"
    layout = soup.find("div", class_="course-layout").text.strip()

    # Return all extracted data as a dictionary
    return {
        "url": course_url,
        "title": title,
        "learning_outcomes": learning_outcomes,
        "topics": topics,
        "layout": layout
    }
