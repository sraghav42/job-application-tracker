import fitz
import re
import spacy
import re
from docx import Document
import dateparser
from datetime import datetime

nlp=spacy.load("en_core_web_sm")

SKILL_LIST={"python", "sql", "fastapi", "docker", "kubernetes", "javascript","java"}

job_title_pattern=re.compile(
    r'\b(?:[A-Z][a-z]+(?:\s[A-Za-z0-9]+){0,3}?\s(?:Engineer|Developer|Scientist|Analyst|Consultant|Architect|Manager|Specialist|Technician|Administrator|Programmer))\b',
    re.IGNORECASE
)

def preprocess_text(text):
    "Cleans and normalizes extracted text"
    text=text.lower()
    text=re.sub(r'\s+',' ',text).strip()
    return text

def extract_skills(text):
    "Extracts skills based on predefined SKILL_LIST"
    words=set(text.split())
    skills=list(words & SKILL_LIST)
    return skills

def extract_experience(text):
    # match=re.search(r'(\d+)\s+years?',text)
    # return f"{match.group(1)} years" if match else "Not specified"

    date_pattern = re.compile(r'(\d{2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|\b\d{4}\b)\s*[-–]\s*(present|\d{2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|\b\d{4}\b)', re.IGNORECASE)

    matches=date_pattern.findall(text)

    total_experience_days=0
    current_date=datetime.today

    for start_date, end_date in matches:
        start=dateparser.parse(start_date)
        end=current_date if "present" in end_date.lower() else dateparser.parse(end_date)

        if isinstance(start,datetime) and isinstance(end, datetime):
            total_experience_days+=(end-start).days

    total_experience_years=total_experience_days/365

    return round(total_experience_years)

def extract_job_titles(text):
    doc=nlp(text)
    
    nlp_titles=[ent.text for ent in doc.ents if ent.label_ in ["JOB_TITLE"]]

    regex_titles=job_title_pattern.findall(text)

    all_titles=list(set(nlp_titles+regex_titles))
    all_titles=[title.strip().title() for title in all_titles]

    return all_titles if all_titles else ["Not specified"]

def parse_resume(text):
    "Extract structured data from resume text"
    text=preprocess_text(text)
    return {
        "skills":extract_skills(text),
        "experience":extract_experience(text),
        "job_titles":extract_job_titles(text)
    }

def extract_text_from_pdf(pdf_path):
    text=""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text+=page.get_text("text") + "\n"
    return text.strip()

def extract_text_from_doc(docx_path):
    doc=Document(docx_path)
    text="\n".join([para.text for para in doc.paragraphs])
    return text.strip()