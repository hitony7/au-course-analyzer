import streamlit as st
from scraper.fetch_courses import fetch_course_links  # Function to get all course URLs from the catalog
from scraper.parse_course import parse_course         # Function to extract course details from a URL
from ai.outline_generator import generate_outline     # Function to generate AI-based course outline
from ai.comparison import compare_outlines            # Function to compute similarity between outlines

# Set title for the web application
st.title("AU Course Analyzer")

# Input field for the AU course catalog base URL
base_url = st.text_input("Enter AU course catalog URL", "https://example.com/courses")

# Button to fetch course links from the given URL
if st.button("Fetch Course Links"):
    course_links = fetch_course_links(base_url)  # Scrape links from the page
    st.write(f"Found {len(course_links)} courses.")  # Display number of courses found
    st.session_state['course_links'] = course_links  # Store in session state to persist across UI actions

# Only show course selection if links have been fetched
if 'course_links' in st.session_state:
    # Dropdown to select one course from the list
    selected_course = st.selectbox("Select a course to analyze", st.session_state['course_links'])

    # Button to perform analysis on the selected course
    if st.button("Analyze Selected Course"):
        # Step 1: Scrape the course page for content
        course_data = parse_course(selected_course)
        st.subheader("Course Info")
        st.json(course_data)  # Display the raw scraped course data

        # Step 2: Use AI to generate a recommended outline
        ai_outline = generate_outline(course_data["title"], course_data["learning_outcomes"])
        st.subheader("AI Generated Outline")
        st.write(ai_outline)

        # Step 3: Compare AI outline vs actual topics using embedding similarity
        actual_outline_text = "\n".join(course_data["topics"])
        similarity_score = compare_outlines(actual_outline_text, ai_outline)

        # Step 4: Show similarity score (0 to 1 range)
        st.subheader("Similarity Score")
        st.write(f"{similarity_score:.2f}")  # e.g., 0.78 indicates high similari_
