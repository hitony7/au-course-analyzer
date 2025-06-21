import streamlit as st
from scraper.fetch_courses import fetch_course_links
from scraper.parse_course import parse_course
from ai.outline_generator import generate_outline
from ai.comparison import compare_outlines

st.title("AU Course Analyzer")

base_url = st.text_input("Enter AU course catalog URL", "https://example.com/courses")

if st.button("Fetch Course Links"):
    course_links = fetch_course_links(base_url)
    st.write(f"Found {len(course_links)} courses.")
    st.session_state['course_links'] = course_links

if 'course_links' in st.session_state:
    selected_course = st.selectbox("Select a course to analyze", st.session_state['course_links'])

    if st.button("Analyze Selected Course"):
        course_data = parse_course(selected_course)
        st.subheader("Course Info")
        st.json(course_data)

        ai_outline = generate_outline(course_data["title"], course_data["learning_outcomes"])
        st.subheader("AI Generated Outline")
        st.write(ai_outline)

        actual_outline_text = "\n".join(course_data["topics"])
        similarity_score = compare_outlines(actual_outline_text, ai_outline)

        st.subheader("Similarity Score")
        st.write(f"{similarity_score:.2f}")