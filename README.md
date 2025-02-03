# AI-Job-Applicator

## Overview
The **AI-Job-Applicator** is an automation tool designed to streamline the job application process by automatically applying to jobs on **Dice.com** based on a given resume and job descriptions. The tool uses natural language processing (NLP) to match the resume with job descriptions, compute similarity scores, and fill out job applications automatically. It also handles the uploading of resumes when required.

## Features
- **Resume Matching**: Uses NLP (e.g., Sentence-BERT) to match your resume with job descriptions based on semantic similarity.
- **Job Title Extraction**: Extracts job titles from job URLs and stores them with timestamps to avoid duplicates.
- **Automated Job Application**: Automatically applies to jobs, including uploading resumes where necessary.
- **Error Handling**: Robust error handling ensures smooth application submissions even in case of unexpected issues.
- **Logout Mechanism**: Logs out of the website once the job application process is complete.

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  - `nltk`
  - `sentence-transformers`
  - `playwright` (or Puppeteer for JavaScript)
  - `datetime`
  - `re`
  - `os`
  - `time`
  
  You can install the necessary Python dependencies using the following command:
  pip install -r requirements.txt

## Functions
**preprocess_text(text)**
Preprocesses the resume or job description by:

Converting text to lowercase.
Removing non-alphabetical characters.
Removing stop words.
Lemmatizing words to their base form.
compute_similarity(resume_text, job_descriptions, job_ids)
Computes similarity between the given resume and job descriptions, returning a list of similarity scores for each job.

**write_job_titles_to_file(page, job_id, url)**
Writes job titles to job_titles.txt with a timestamp. It avoids duplicate job titles by checking the existing file.

**evaluate_and_apply(page, val)**
Evaluates the job application page and clicks the "Apply" button if available. If the resume is not uploaded, it initiates the upload process.

**apply_and_upload_resume(page, val)**
Handles resume uploading and job application submission.

**logout_and_close(page, browser)**
Logs out from the Dice website and closes the browser.
