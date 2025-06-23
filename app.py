import streamlit as st
from scraper.fetch_courses import fetch_course_metadata
from scraper.parse_course import parse_course
from ai.outline_generator import generate_outline
from ai.comparison import compare_outlines
from collections import defaultdict

st.title("AU Course Analyzer")

# Input: AU catalog URL
base_url = st.text_input("Enter AU course catalog URL", "")

# Fetch metadata from AU catalog
if st.button("Fetch Course Links"):
    course_links = fetch_course_metadata(base_url)
    st.write(f"Found {len(course_links)} courses.")
    st.session_state["course_links"] = course_links

# If courses are available
if "course_links" in st.session_state:
    # Step 1: Group courses by prefix (e.g., COMP, CMIS)
    prefix_map = defaultdict(list)
    for course in st.session_state["course_links"]:
        prefix = course["course_code"].split()[0]
        prefix_map[prefix].append(course)

    # Step 2: User selects a prefix
    selected_prefix = st.selectbox("Select a course prefix", sorted(prefix_map.keys()))

    # Step 3: Show course options under that prefix
    course_labels = [
        f"{course['course_code']}: {course['course_name']}"
        for course in prefix_map[selected_prefix]
    ]
    selected_label = st.selectbox("Select a course to analyze", course_labels)

    # Step 4: Find the selected course
    selected_course = next(
        (
            course
            for course in prefix_map[selected_prefix]
            if f"{course['course_code']}: {course['course_name']}" == selected_label
        ),
        None,
    )

    if st.button("Analyze Selected Course"):
        # Step 5: Scrape course details
        course_data = parse_course(selected_course["url"])
        st.subheader("Course Info")
        st.json(course_data)

        # Step 6: Generate AI outline
        ai_outline = generate_outline(course_data)
        st.subheader("AI Generated Outline")
        st.write(ai_outline)

        # Step 7: Compare outlines
        actual_outline_text = "\n".join(course_data["topics"])
        similarity_score = compare_outlines(actual_outline_text, ai_outline)

        st.subheader("Similarity Score")
        st.write(f"{similarity_score:.2f}")
