# Install necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Title and description
st.title("Job Search Scraper")
st.write("""
This app scrapes Google to find job postings based on the role you input. It also uses an open-source LLM for additional analysis, 
such as summarizing job descriptions or extracting key skills.
""")

# Input: Job Role
job_role = st.text_input("Enter the job role (e.g., TPM, Data Scientist):", placeholder="Type a job role here...")

# Scraper function
def scrape_google_jobs(job_role):
    """
    Scrapes Google Search for job postings related to the given role.
    """
    try:
        # Format the search query
        query = f"{job_role} jobs"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws"

        # Send a GET request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        job_results = []

        # Extract job postings
        for result in soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd"):
            title = result.get_text()
            link = result.find_parent("a")["href"]
            job_results.append({"title": title, "link": link})

        return job_results

    except requests.exceptions.RequestException as e:
        st.error("Error fetching data from Google. Please try again later.")
        return []

# NLP function for summarization
def summarize_text(text):
    """
    Summarizes the given text using a pre-trained Hugging Face model.
    """
    summarizer = pipeline("summarization", model="t5-small")
    summary = summarizer(text, max_length=50, min_length=10, do_sample=False)
    return summary[0]["summary_text"]

# Button to trigger scraping
if st.button("Find Jobs"):
    if job_role:
        st.write(f"Searching for jobs related to: **{job_role}**")
        jobs = scrape_google_jobs(job_role)

        if jobs:
            st.write("### Found Job Postings:")
            for job in jobs:
                st.markdown(f"- **{job['title']}** - [Link]({job['link']})")
        else:
            st.write("No job postings found. Please try a different query.")
    else:
        st.error("Please enter a job role.")

# Optional NLP Analysis
if st.checkbox("Enable NLP Analysis"):
    st.write("### NLP Analysis (e.g., Summarization):")
    input_text = st.text_area("Paste a job description or content here:")
    if st.button("Summarize"):
        if input_text.strip():
            summary = summarize_text(input_text)
            st.write("#### Summary:")
            st.write(summary)
        else:
            st.error("Please enter some text to summarize.")

