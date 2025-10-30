from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class JobApplicationAutomationSchema(BaseModel):
    job_application: str
    application_send_date: datetime
    is_mail_sent: bool = Field(default=False)


class JobApplicationAutomationResponse(JobApplicationAutomationSchema):
    id: str = Field(default_factory=str, alias="_id")
    model_config = ConfigDict(populate_by_name=True)
