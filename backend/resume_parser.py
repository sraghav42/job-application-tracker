import fitz
import spacy
import re
from docx import Document

nlp=spacy.load("en_core_web_sm")

SKILL_LIST={"python", "sql", "fastapi", "docker", "kubernetes", "javascript","java"}

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
    match=re.search(r'(\d+)\s+years?',text)
    return f"{match.group(1)} years" if match else "Not specified"

def extract_job_titles(text):
    doc=nlp(text)
    job_titles=[ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return job_titles if job_titles else ["Not specified"]

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