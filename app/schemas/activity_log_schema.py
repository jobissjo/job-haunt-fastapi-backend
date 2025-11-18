from pydantic import BaseModel

class ActivityLogSchema(BaseModel):
    type :str
    message:str