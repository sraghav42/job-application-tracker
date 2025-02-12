from fastapi import APIRouter, UploadFile, File, HTTPException
import resume_parser as rp
import shutil
import os

router = APIRouter(prefix="/resume", tags=["Resume Parsing"])

UPLOAD_DIR = "/Coding Projects/job-application-tracker/uploaded_resumes/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get file extension
    file_ext = file.filename.split(".")[-1].lower()

    # Process based on file type
    if file_ext == "pdf":
        extracted_text = rp.extract_text_from_pdf(file_path)
    elif file_ext in ["doc", "docx"]:
        extracted_text = rp.extract_text_from_docx(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    parsed_data=rp.parse_resume(extracted_text)

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "parsed_data": parsed_data,
    }
