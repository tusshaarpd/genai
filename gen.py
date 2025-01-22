# Install required libraries
import streamlit as st
import requests

# Title and description
st.title("Job Search App")
st.write("""
This app searches Google for job postings based on the role you input, using SerpAPI for reliable results.
""")

# Input: Job Role
job_role = st.text_input("Enter the job role (e.g., TPM, Data Scientist):", placeholder="Type a job role here...")

# Input: Location (optional)
job_location = st.text_input("Enter the job location (optional):", placeholder="Type a location here...")

# Function to search Google using SerpAPI
def search_jobs_with_serpapi(query, location):
    """
    Fetches job postings from Google using SerpAPI.
    """
    api_key = "your_serpapi_api_key"  # Replace with your actual SerpAPI key
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_jobs",  # Specify that we're searching for Google Jobs
        "q": query,
        "location": location,
        "api_key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        # Extract job postings
        jobs = results.get("jobs_results", [])
        return jobs

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

# Button to trigger job search
if st.button("Search Jobs"):
    if job_role:
        st.write(f"Searching for jobs related to: **{job_role}**")
        location = job_location if job_location else "Worldwide"
        jobs = search_jobs_with_serpapi(job_role, location)

        if jobs:
            st.write("### Job Postings Found:")
            for job in jobs:
                st.markdown(f"""
                - **{job['title']}**  
                  Location: {job.get('location', 'N/A')}  
                  Company: {job.get('company_name', 'N/A')}  
                  [Job Link]({job['link']})
                """)
        else:
            st.write("No job postings found. Please try a different query.")
    else:
        st.error("Please enter a job role.")

