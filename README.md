# AU Course Analyzer

This project is a Python-based web application for analyzing Athabasca University (AU) courses using a combination of web scraping and generative AI.

## 🧠 Features

- Scrape AU course listings from the public website
- Extract key information: course title, learning outcomes, topics, and layout
- Generate an AI-suggested course outline using OpenAI GPT-4o
- Compare the AI-generated outline with the real course topics
- Display similarity score and insights
- Easy-to-use Streamlit-based web interface

## Project Requirements

- You may use any Python libraries you need
- The analysis can be done either for all courses offered, or courses in a specific subject, or a particular course
- deliverables should include all the code for the project
- report/documentation.

##Python Libaray used(Using Python 3)

- beautifulsoup4 – Parses HTML to extract course content.
- requests – Sends HTTP requests to fetch static web pages.
- selenium – Automates browser interaction for dynamic web content.
- webdriver-manager – Auto-manages browser drivers for Selenium.
- openai – Connects to OpenAI API to generate AI course outlines.
- sentence-transformers – Encodes text into vector embeddings for comparison.
- scikit-learn – Calculates cosine similarity between outlines.
- python-dotenv – Loads API keys securely from .env files.

## 🚀 Getting Started

### 1. Clone or Download

You can download the ZIP or clone this repo:

```bash
git clone https://github.com/hitony7/au-course-analyzer.git
cd au-course-analyzer
```

### 2. Install Dependencies

Create a virtual environment and install requirements:

```bash
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Add OpenAI Key

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

## 🔧 Project Structure

```
au-course-analyzer/
├── app.py                   # Main Streamlit app
├── requirements.txt         # Required Python libraries
├── parsed_courses/          # Parsed indivdual courses
├── renderd_pages/           # Full HTML DOC of indivdual courses used for debugging
├── scraper/
│   ├── fetch_courses.py     # Fetches course URLs
│   ├── parse_course.py      # Parses details from a course page
├── ai/
│   ├── outline_generator.py # Uses GPT to generate outline
│   ├── comparison.py        # Computes similarity score
├── data/                    # (Optional) Local storage for scraped data
├── .env                     # API keys (not included in repo)
├── au_course.json           # Course Directoray
├── au_full_page.html        # Full HTML DOC of courses from https://www.athabascau.ca/course/index.html?/undergraduate
├── README.md                # This file
```

### Future changes

- implement caching for courses, check date of json and if it's not too old then reuse it
- Loading takes long, have better indicators for user
