import smtplib
import mimetypes
import os
from email.message import EmailMessage


def send_email_with_attachment(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    from_name: str,
    from_email: str,
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str,
) -> None:
    """
    Envia um email com anexo via SMTP.
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg.set_content(body)

    file_name = os.path.basename(attachment_path)
    ctype, encoding = mimetypes.guess_type(attachment_path)

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    with open(attachment_path, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype=maintype,
            subtype=subtype,
            filename=file_name,
        )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)