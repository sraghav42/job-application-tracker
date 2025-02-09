from fastapi import APIRouter,Depends,HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from models import JobApplication
from schemas import JobApplicationCreate,JobApplicationUpdate
from typing import List

router=APIRouter(prefix="/jobs",tags=["Job Applications"])

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

#POST endpoint for create job application
@router.post("/",response_model=JobApplicationCreate)
def create_job_application(job:JobApplicationCreate, db:Session=Depends(get_db)):
    new_job=JobApplication(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

#GET all job applications
@router.get("/",response_model=List[JobApplicationCreate])
def get_jobs(db:Session=Depends(get_db)):
    return db.query(JobApplication).all()

#GET a specific job application by req_id
@router.get("/{req_id}",response_model=JobApplicationCreate)
def get_job(req_id:str,db:Session=Depends(get_db)):
    job=db.query(JobApplication).filter(JobApplication.req_id==req_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    return job

#UPDATE a job application (PUT)
@router.put("{job_id}",response_model=JobApplicationCreate)
def update_job(job_id:int,job_update:JobApplicationUpdate,db:Session=Depends(get_db)):
    job=db.query(JobApplication).filter(JobApplication.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    
    for key,value in job_update.dict(exclude_unset=True).items():
        setattr(job,key,value)
    
    db.commmit()
    db.refresh(job)
    return job

#DELETE a job application
@router.delete("/{job_id}")
def delete_job(job_id:int, db:Session=Depends(get_db)):
    job=db.query(JobApplication).filter(JobApplication.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    
    db.delete()
    db.commit()
    return {"message":"Job deleted successfully"}