from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class JobApplicationCreate(BaseModel):
    company:str=Field(...,example="Google")
    role:str=Field(...,example="Software Engineer")
    status:Optional[str]="Applied"
    applied_at:Optional[datetime]=datetime.utcnow()
    req_id:Optional[str]=None

    class Config:
        from_attributes=True


class JobApplicationUpdate(BaseModel):
    status:Optional[str]=None

    class Config:
        from_attributes=True