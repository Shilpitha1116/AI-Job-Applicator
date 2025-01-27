from playwright.sync_api import sync_playwright
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import time
import logging
import openai
from PyPDF2 import PdfReader
from flask import Flask, jsonify, request
from datetime import datetime
from zoneinfo import ZoneInfo
from DiceAutomation import(
    login,
    extract_resume_text,
    generate_search_query_components,
    perform_job_search,
    extract_job_ids,
    scrape_job_descriptions,
    preprocess_text,
    compute_similarity,
    write_job_titles_to_file,
    evaluate_and_apply,
    apply_and_upload_resume,
    logout_and_close
)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Ensure the upload folder exists
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Main Workflow
@app.route('/automate-dice', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                email = request.form.get('email')
                password = request.form.get('password')
                threshold = request.form.get('threshold')
                location = request.form.get('location')

                if 'resume' not in request.files:
                    return jsonify({"error": "No resume file provided"}), 400
                resume = request.files['resume']
                if resume.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                if not resume.filename.lower().endswith('.pdf'):
                    return jsonify({"error": "Invalid file format. Only .pdf files are allowed."}), 400
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
                resume.save(resume_path)

                resume_text = extract_resume_text(resume_path)

                login(page, email, password)

                job_titles, skills = generate_search_query_components(resume_text)
                #location = "United States"
                search_query = f'({" OR ".join(job_titles)}) OR ({" OR ".join(skills)})'
                #search_query = ("Java Full-Stack Developer")
                logger.info(f"Generated search query: {search_query}")
                perform_job_search(page, search_query, location)

                job_ids = extract_job_ids(page)

                if job_ids:
                    job_descriptions = scrape_job_descriptions(page, job_ids)
                else:
                    logger.error("No job IDs were extracted. Skipping job description scraping.")

                similarity_results = compute_similarity(resume_text, job_descriptions, job_ids)

                # Apply for jobs that meet the similarity threshold
                for job_id, similarity in similarity_results:
                    if similarity >= float(threshold):
                        print(f"Applying for job {job_id} with similarity {similarity:.2f}")
                        write_job_titles_to_file(page, job_id, "https://www.dice.com/jobs")
                    else:
                        print(f"Skipped job {job_id} with similarity {similarity:.2f}")

                logout_and_close(page, browser)

            return {"status": "success", "message": "Automation completed successfully."}, 200
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {"status": "error", "message": f"An error occurred: {str(e)}"}, 500


# Run the main function
if __name__ == "__main__":
    app.run(debug=False)
