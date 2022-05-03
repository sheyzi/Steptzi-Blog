import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from config.settings import settings
from app.schemas import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_FROM_NAME=settings.PROJECT_TITLE,
    TEMPLATE_FOLDER=os.path.join(os.getcwd(), "app/email_templates"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


def send_email(
    background_tasks: BackgroundTasks,
    subject: str,
    email: EmailSchema,
    template_name: str,
):
    message = MessageSchema(
        subject=subject, recipients=email.emails, template_body=email.body
    )

    fm = FastMail(config=conf)
    background_tasks.add_task(fm.send_message, message, template_name=template_name)
