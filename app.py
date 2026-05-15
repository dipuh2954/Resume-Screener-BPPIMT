from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import sqlite3
import json
import os
import re
from datetime import datetime
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv

# ------------------ SETUP ------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("❌ GOOGLE_API_KEY not found! AI insights will be disabled.")

model = genai.GenerativeModel("gemini-1.5-flash") if API_KEY else None

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=basedir)
CORS(app)

DB_PATH = os.path.join(basedir, 'resume_scanner.db')


# ------------------ DATABASE ------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screening_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                job_description TEXT,
                results TEXT,
                resume_count INTEGER,
                timestamp TEXT
            )
        ''')
        conn.commit()

# ADD THIS EXACT LINE HERE, FLUSH AGAINST THE LEFT WALL:
init_db()

# ------------------ PDF EXTRACTION ------------------
def extract_text_from_pdf(file_storage):
    """Extract text from an uploaded PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file_storage) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + " "
    except Exception as e:
        print("PDF Error:", e)
    return text.strip()


# ------------------ SKILL HELPERS ------------------
def extract_jd_keywords(jd_text, top_n=30):
    """Extract top keywords from the job description using TF-IDF."""
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=top_n,
            ngram_range=(1, 2)       # include bigrams like "machine learning"
        )
        vectorizer.fit([jd_text])
        return list(vectorizer.vocabulary_.keys())
    except Exception:
        return []

#it helps to detect matched and missing skills 
def get_matched_and_missing(resume_text, jd_keywords):
    """Return (matched_skills, missing_skills) lists based on keyword presence."""
    resume_lower = resume_text.lower()
    matched  = [kw for kw in jd_keywords if kw.lower() in resume_lower]
    missing  = [kw for kw in jd_keywords if kw.lower() not in resume_lower]
    return matched[:20], missing[:20]


def highlight_keywords(text, keywords):
    """Wrap matched keywords in <mark> tags for highlighted resume view."""
    highlighted = text
    for kw in sorted(keywords, key=len, reverse=True):   # long phrases first
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        highlighted = pattern.sub(lambda m: f'<mark>{m.group()}</mark>', highlighted)
    return highlighted


def detect_experience_level(text):
    """
    Heuristic: scan resume text for year mentions.
    Returns 'fresher' | 'mid' | 'senior'.
    """
    matches = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)?',
        text.lower()
    )
    years = max((int(m) for m in matches), default=0)
    if years >= 5:
        return "senior"
    elif years >= 2:
        return "mid"
    else:
        return "fresher"


# ------------------ ROUTES ------------------

# Serve upload page
@app.route('/')
def serve_index():
    return send_from_directory(basedir, 'index.html')


# Serve static files (CSS, JS, HTML)
@app.route('/<path:path>')
def serve_static(path):
    blocked = ['.env', 'app.py', 'database.py', 'resume_scanner.db', 'history.db']
    if path in blocked:
        return abort(403)
    return send_from_directory(basedir, path)


# GET /history — return all past sessions
@app.route('/history', methods=['GET'])
def get_history():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM screening_history ORDER BY id DESC")
            rows = cursor.fetchall()

        history = []
        for row in rows:
            history.append({
                "id":              row[0],
                "job_title":       row[1],
                "job_description": row[2],
                "results":         json.loads(row[3]),
                "resume_count":    row[4],
                "timestamp":       row[5]
            })

        return jsonify({"success": True, "history": history})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# DELETE /delete/<id> — remove one history session
@app.route('/delete/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM screening_history WHERE id = ?", (session_id,)
            )
            conn.commit()
        return jsonify({"success": True, "deleted_id": session_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# POST /screen — upload JD + resumes, run AI screening
@app.route('/screen', methods=['POST'])
def screen_resumes():
    try:
        job_title       = request.form.get('job_title', 'Untitled').strip()
        job_description = request.form.get('job_description', '').strip()
        files           = request.files.getlist('resumes')

        if not files or not job_description:
            return jsonify({"success": False, "message": "Missing job description or resume files."}), 400

        # Pre-compute JD keywords once for all resumes
        jd_keywords = extract_jd_keywords(job_description, top_n=30)

        processed_results = []
        vectorizer = TfidfVectorizer(stop_words='english')

        for idx, file in enumerate(files):
            resume_text = extract_text_from_pdf(file)
            if not resume_text:
                # Skip unreadable PDFs (scanned images, etc.)
                continue

            # ── TF-IDF match score (0–100) ──────────────────────────
            try:
                tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
                score = int(
                    cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
                )
            except Exception:
                score = 0

            # ── Skill matching ──────────────────────────────────────
            matched_skills, missing_skills = get_matched_and_missing(
                resume_text, jd_keywords
            )

            # ── Highlighted resume text (first 3000 chars) ──────────
            preview_text   = resume_text[:3000]
            highlighted    = highlight_keywords(preview_text, matched_skills)

            # ── Experience level ────────────────────────────────────
            level = detect_experience_level(resume_text)

            # ── Gemini AI insight ───────────────────────────────────
            ai_insight = "No AI analysis available."
            if API_KEY and model:
                try:
                    prompt = (
                        f"Job Role: {job_title}\n"
                        f"Job Description (excerpt): {job_description[:300]}\n"
                        f"Resume (excerpt): {resume_text[:800]}\n\n"
                        "Give a concise 1-sentence hiring verdict for this candidate."
                    )
                    response = model.generate_content(prompt)
                    ai_insight = response.text.strip()
                except Exception as e:
                    print("Gemini Error:", e)

            # ── Derive display name from filename ───────────────────
            base_name = os.path.splitext(file.filename)[0]
            display_name = re.sub(r'[_\-]+', ' ', base_name).title()

            processed_results.append({
                "id":               idx + 1,
                "name":             display_name,
                "filename":         file.filename,
                "score":            score,
                "level":            level,
                "insight":          ai_insight,
                "matched_skills":   matched_skills,
                "missing_skills":   missing_skills,
                "highlighted_text": highlighted,
                "raw_text":         preview_text,
                "rank":             0    # filled after sort below
            })

        # Sort by score descending, then assign rank
        processed_results.sort(key=lambda x: x['score'], reverse=True)
        for rank_idx, candidate in enumerate(processed_results):
            candidate['rank'] = rank_idx + 1

        # ── Common skills gap (keywords missing from most resumes) ──
        gap_counter = {}
        for candidate in processed_results:
            for skill in candidate['missing_skills']:
                gap_counter[skill] = gap_counter.get(skill, 0) + 1
        common_gaps = sorted(gap_counter, key=lambda k: gap_counter[k], reverse=True)[:12]

        # ── Save session to DB ──────────────────────────────────────
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO screening_history
                    (job_title, job_description, results, resume_count, timestamp)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (
                    job_title,
                    job_description,
                    json.dumps(processed_results),
                    len(processed_results),
                    datetime.now().isoformat()
                )
            )
            conn.commit()

        return jsonify({
            "success":     True,
            "candidates":  processed_results,
            "common_gaps": common_gaps,
            "count":       len(processed_results)
        })

    except Exception as e:
        print("Screen error:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# ------------------ RUN ------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000, threaded=True)
