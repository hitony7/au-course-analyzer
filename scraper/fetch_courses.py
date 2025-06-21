import requests
from bs4 import BeautifulSoup

def fetch_course_links(base_url):
    # Send an HTTP GET request to the course catalog page
    response = requests.get(base_url)
    
    # Parse the response HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize an empty list to store the course links
    course_links = []

    # Select all anchor tags with the class "course-link"
    # NOTE: You may need to update the selector depending on AU's actual site structure
    for a_tag in soup.select("a.course-link"):
        href = a_tag.get("href")  # Extract the href attribute from the anchor tag
        if href:
            course_links.append(href)  # Add the link to the list if it's valid

    # Return the list of course URLs
    return course_links
