import os
import google.generativeai as genai
from fastapi import APIRouter,HTTPException
from resume_parser import parse_resume,extract_text_from_doc,extract_text_from_pdf

API_KEY=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

router=APIRouter(prefix="/cover_letter", tags=["Cover Letter Generator"])

@router.post("/generate/")
async def generate_cover_letter(filename:str, job_description:str):
    try:
        UPLOAD_DIR="uploaded_resumes"
        file_path=os.path.join(UPLOAD_DIR,filename)

        if not os.path.exists(file_path):
            raise HTTPException(status=404,detail="Resume file not found")
        
        file_ext = filename.split(".")[-1].lower()
        if file_ext == "pdf":
            resume_text = extract_text_from_pdf(file_path)
        elif file_ext in ["doc", "docx"]:
            resume_text = extract_text_from_doc(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        resume_data=parse_resume(resume_text)

        prompt=f"""
        You are a professional career assistant. Generate a well-formatted, editable cover letter using the resume and job description.

        **Resume Details:**
        - Job Title: {resume_data.get("job_titles", ["Unknown"])[0]}
        - Skills: {", ".join(resume_data.get("skills", []))}
        - Experience: {resume_data.get("experience", "0")} years

        **Job Description:**
        {job_description}

        **Cover Letter Guidelines:**
        - Include a professional greeting ("Dear Hiring Manager,").
        - Write a strong introduction mentioning enthusiasm for the role.
        - Highlight relevant skills and experience.
        - Add a closing statement expressing interest in further discussion.
        - Keep it concise and well-structured.

        **Output format:**
        - Proper paragraph spacing
        - No excessive repetition
        - 3-5 short paragraphs
        - Professional yet engaging tone
        """

        model=genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
        response=model.generate_content(prompt)

        return {"cover_letter":response.text, "editable":True}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))