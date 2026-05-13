# AI-Powered Resume Screener 📄🤖

A full-stack web application designed to automate resume screening using Natural Language Processing and Google's Gemini AI. 

## Features
* **PDF Text Extraction:** Automatically reads and parses uploaded resumes.
* **Smart Scoring:** Ranks candidates against a provided Job Description using TF-IDF.
* **AI Insights:** Generates a one-sentence hiring verdict for each candidate.
* **Skills Gap Analysis:** Highlights exact keywords missing from applicant resumes.

## Tech Stack
* **Backend:** Python, Flask, SQLite
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **AI/ML:** Scikit-Learn, Google Generative AI (Gemini 1.5 Flash), pdfplumber

## Local Setup Instructions
1. Clone the repository:
   `git clone https://github.com/your-username/resume-screener.git`
2. Navigate to the project folder:
   `cd resume-screener`
3. Create a virtual environment:
   `python3 -m venv venv`
4. Activate the virtual environment:
   * Mac/Linux: `source venv/bin/activate`
   * Windows: `venv\Scripts\activate`
5. Install the dependencies:
   `pip install -r requirements.txt`
6. Create a `.env` file in the root directory and add your Gemini API Key:
   `GOOGLE_API_KEY=your_api_key_here`
7. Run the application:
   `python app.py`