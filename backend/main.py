from fastapi import FastAPI
from routes import job_routes,resume_routes,match_routes,cover_letter_routes

app=FastAPI()
app.include_router(job_routes.router)
app.include_router(resume_routes.router)
app.include_router(match_routes.router)
app.include_router(cover_letter_routes.router)

@app.get("/")
def read_root():
    return {"message":"Job Tracker API is running!"}