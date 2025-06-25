import streamlit as st
from scraper.fetch_courses import fetch_course_metadata
from scraper.parse_course import parse_course
from ai.outline_generator import generate_outline
from ai.comparison import compare_outlines, compare_outlines_keywords
from collections import defaultdict
import pandas as pd

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
        actual_outline_text = "\n".join(
            [
                course_data.get("course_title", ""),
                course_data.get("outline", ""),
                course_data.get("learning_outcomes", ""),
            ]
        )

        similarity_score = compare_outlines(actual_outline_text, ai_outline)

        st.subheader("Similarity Score")
        st.write(f"**{similarity_score:.2f}**")

        if similarity_score > 0.8:
            st.success(
                "High similarity: The AI-generated outline is closely aligned with the actual course content."
            )
        elif similarity_score > 0.5:
            st.info(
                "Moderate similarity: The AI outline shares some concepts with the real outline but may miss key areas."
            )
        else:
            st.warning(
                "Low similarity: The AI outline differs significantly from the actual course content. Review is recommended."
            )

        with st.expander("ℹ️ How this score is calculated"):
            st.markdown(
                """
                The similarity score is based on **cosine similarity** between the AI-generated outline and the actual course outline.

                Both outlines are first converted into high-dimensional vectors using a transformer model called **MiniLM**.

                These embeddings capture the **semantic meaning** of text (i.e., what it's about), not just keywords. Cosine similarity then measures how closely aligned the two vectors are:

                - **1.0** = perfect semantic match  
                - **0.0** = no semantic similarity  
                
                For more information on the MiniLM model used for semantic embeddings, visit:
                https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
                
                """
            )

        # Keyword comparison
        result = compare_outlines_keywords(actual_outline_text, ai_outline)

        st.subheader("Keyword Similarity Score")
        with st.expander("ℹ️ How this score is calculated"):
            st.markdown(
                """
            The keyword similarity score is based on **Jaccard similarity**, which measures the overlap between two sets of keywords.

            For each outline, we first extract keywords by tokenizing the text, removing stopwords, and counting the occurrences of each word. The top 10 most common words are considered the most representative keywords for each outline.

            The Jaccard similarity is then calculated as the size of the intersection (common keywords) divided by the size of the union (all unique keywords) of the two sets. This score ranges from:

            - **1.0** = all keywords are identical  
            - **0.0** = no keywords are shared  

            """
            )
        st.write(f"{result['similarity_score']:.2f}")

        st.subheader("Word Counts")
        st.write(f"Actual Outline Word Count: {result['actual_word_count']}")
        st.write(f"AI Outline Word Count: {result['ai_word_count']}")

        # Prepare data for side-by-side display
        keywords_df = pd.DataFrame(
            {
                "Actual Keywords": [word for word, _ in result["actual_top_words"]],
                "Actual Count": [count for _, count in result["actual_top_words"]],
                "AI Keywords": [word for word, _ in result["ai_top_words"]],
                "AI Count": [count for _, count in result["ai_top_words"]],
            }
        )

        st.subheader("Top 10 Keywords Comparison")
        st.table(keywords_df)
