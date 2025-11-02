from app.schemas.user_mail_settings import EmailSettings
from email.message import EmailMessage
import aiosmtplib
from typing import Optional, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from app.settings import settings
from datetime import datetime

class EmailUtils:
    @staticmethod
    async def send_mail(
        user_id: str,
        email_setting: EmailSettings,
        to_email: str,
        subject: str,
        template_name: str,
        template_data: Optional[Dict] = None,
        job_application_id: Optional[str] = None,
    ):
        try:
            # 1️⃣ Load the Jinja2 environment
            template_dir = os.path.join(settings.BASE_DIR, "app", "templates")
            env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(["html", "xml"]),
            )

            # 2️⃣ Load and render the template
            template = env.get_template(template_name)
            html_content = template.render(template_data or {})

            # 3️⃣ Create the email message
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = email_setting.get("from_email")
            message["To"] = to_email
            message.set_content("Your email client does not support HTML.")
            message.add_alternative(html_content, subtype="html")

            # 4️⃣ Send asynchronously
            await aiosmtplib.send(
                message,
                hostname=email_setting.get("host"),
                port=email_setting.get("port"),
                username=email_setting.get("username"),
                password=email_setting.get("password"),
                start_tls=True, 
            )

        except Exception as e:
            raise e
    
    async def get_basic_template_data(self)->dict[str,str]:
        return {
            "current_year": datetime.now().year,
            "company_name": settings.COMPANY_NAME,

        }
