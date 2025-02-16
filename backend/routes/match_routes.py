from fastapi import APIRouter, HTTPException
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity
from resume_parser import extract_text_from_doc,extract_text_from_pdf,parse_resume
import os
import re
import spacy

nlp=spacy.load("en_core_web_sm")
model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
UPLOAD_DIR="uploaded_resumes"

router=APIRouter(prefix="/match", tags=["Job Matching"])


@router.get("/list_resumes/")
async def list_uploaded_resumes():
    try:
        if not os.path.exists(UPLOAD_DIR):
            return {"uploaded_resumes":[]}
        resumes=[f for f in os.listdir(UPLOAD_DIR) if f.endswith((".pdf",".docx"))]
        return {"uploaded_resumes":resumes}
    except Exception as e:
        return {"error":str(e)}

def get_text_embedding(text):
    return model.encode(text,convert_to_tensor=True)

def compute_similarity(embedding1, embedding2):
    embedding1=embedding1.unsqueeze(0) if len(embedding1.shape) ==1 else embedding1
    embedding2=embedding2.unsqueeze(0) if len(embedding2.shape) ==1 else embedding2
    return cosine_similarity(embedding1,embedding2).item()

def extract_job_requirements(job_text):
    """Extract job title, required skills, and experience from a job description."""
    doc = nlp(job_text)

    job_title = "Unknown"
    for ent in doc.ents:
        if ent.label_ in ["JOB_TITLE", "ORG"]:
            job_title = ent.text
            break

    # **Use NLP to find relevant skills instead of static regex**
    skills = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.is_alpha:
            skills.append(token.text.lower())

    skills = list(set(skills))  # Remove duplicates

    # Extract experience required
    experience_match = re.search(r'(\d+)\+?\s*(years|yrs|Yrs|Years) of experience', job_text, re.IGNORECASE)
    experience_required = int(experience_match.group(1)) if experience_match else 0  # Default to 0 if not found

    return {
        "title": job_title.lower(),
        "skills": skills,
        "experience_required": experience_required
    }


def jaccard_similarity(set1, set2):
    """Calculate Jaccard Similarity between two sets."""
    set1, set2 = set(set1), set(set2)  # Ensure inputs are sets
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def compute_weighted_similarity(resume_text, job_text):
    """Calculate similarity score using weighted factors."""
    resume_embedding = get_text_embedding(resume_text)
    job_embedding = get_text_embedding(job_text)

    base_similarity = compute_similarity(resume_embedding, job_embedding)

    resume_data = parse_resume(resume_text)
    job_data = extract_job_requirements(job_text)

    skills_match = jaccard_similarity(resume_data['skills'], job_data['skills'])

    # Improve title matching by checking partial matches
    resume_titles = [title.lower() for title in resume_data.get('job_titles', [])]
    job_title = job_data.get('title', "").lower()

    title_match = 0.5  # Default to partial match
    for title in resume_titles:
        if title in job_title or job_title in title:
            title_match = 1.0  # Full match found
            break

    # Ensure experience is numeric and avoid division by zero
    resume_experience = int(resume_data.get('experience', 0))  
    job_experience = max(int(job_data.get('experience_required', 0)), 1)

    experience_match = min(resume_experience / job_experience, 1.0)

    final_score = (base_similarity*0.1) + (skills_match * 0.6) + (title_match * 0.1) + (experience_match * 0.2)
    return final_score


@router.post("/match_jobs")
async def match_jobs(filename:str, job_descriptions:list[str], top_n:int=5):
    try:
        file_path=os.path.join(UPLOAD_DIR,filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Resume file not found")
        
        #extract text based on file type
        file_ext=filename.split(".")[-1].lower()
        if file_ext=="pdf":
            with open(file_path,"rb") as f:
                resume_text=extract_text_from_pdf(f)
        elif file_ext==".docx":
            with open(file_path,"rb") as f:
                resume_text=extract_text_from_doc(f)
        else:
            raise HTTPException(status_code=400, detail="Unsupported fileformat")
        

        scores=[(job,compute_weighted_similarity(resume_text,job)) for job in job_descriptions]
        ranked_jobs=sorted(scores,key=lambda x:x[1], reverse=True)[:top_n]
        return {"top_matches":[{"job_description":job, "score":score} for job,score in ranked_jobs]}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))