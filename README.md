# AI-Powered Resume Screener (BPPIMT) 📄🤖

A full-stack web application designed to automate resume screening using Natural Language Processing and Google's Gemini AI. Built collaboratively as an academic project.

## 🌐 Live Demo
*(Once deployed, replace this text with your Render live link: e.g., `https://resume-screeener-bppimt.onrender.com`)*

## ✨ Features
* **PDF Text Extraction:** Automatically reads and parses uploaded resumes.
* **Smart Scoring:** Ranks candidates against a provided Job Description using TF-IDF.
* **AI Insights:** Generates a one-sentence hiring verdict for each candidate using Gemini 1.5 Flash.
* **Skills Gap Analysis:** Highlights exact keywords missing from applicant resumes.
* **History Tracking:** Automatically saves previous screening sessions for later review.

## 🛠 Tech Stack
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Backend:** Python, Flask, SQLite
* **AI/ML:** Scikit-Learn, Google Generative AI, pdfplumber
* **Deployment:** Render (Gunicorn)

## 💻 Local Setup Instructions (For Teammates)
If you are pulling this code to work on it locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Resume-Screeener-BPPIMT.git](https://github.com/your-username/Resume-Screeener-BPPIMT.git)
