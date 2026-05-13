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

```

2. **Navigate to the project folder:**
```bash
cd Resume-Screeener-BPPIMT

```


3. **Create and activate a virtual environment:**
* **Mac/Linux:** `python3 -m venv venv && source venv/bin/activate`
* **Windows:** `python -m venv venv && venv\Scripts\activate`


4. **Install the dependencies:**
```bash
pip install -r requirements.txt

```


5. **Set up the API Key:**
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GOOGLE_API_KEY=your_api_key_here

```


6. **Run the application:**
```bash
python app.py

```


*The app will be available in your browser at `http://127.0.0.1:5000*`

```

**One quick fix before you save it:** Make sure to swap out `your-username` in the clone link (under step 1) with your actual GitHub username!

```
