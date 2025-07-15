import smtplib
import os
import random
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import time
from auth import *


logging.basicConfig(
    filename="email_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s"
)
html_folder = "html"
img_folder = "img"
pdf_folder = "pdf"
body_folder = "body"


def get_random_file(folder):
    files = os.listdir(folder)
    return os.path.join(folder, random.choice(files))


def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()


def load_smtp_credentials(file_path):
    credentials = []
    with open(file_path, "r") as file:
        for line in file:
            credentials.append(tuple(line.strip().split(":")))
    return credentials


def load_recipients(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def save_recipients(file_path, recipients):
    with open(file_path, "w") as file:
        for recipient in recipients:
            file.write(f"{recipient}\n")


def save_failed_smtp(file_path, smtp_info):
    with open(file_path, "a") as file:
        file.write(f"{smtp_info[0]}:{smtp_info[1]}:{smtp_info[2]}\n")


def save_failed_email(file_path, recipient_email):
    with open(file_path, "a") as file:
        file.write(f"{recipient_email}\n")


def load_subject(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return random.choice(lines).strip()


def remove_invalid_smtp(file_path, smtp_info):
    smtp_credentials = load_smtp_credentials(file_path)
    smtp_credentials = [cred for cred in smtp_credentials if cred != smtp_info]
    with open(file_path, "w") as file:
        for cred in smtp_credentials:
            file.write(f"{cred[0]}:{cred[1]}\n")


def send_email(
    smtp_info,
    subject,
    body_text,
    body_html=None,
    attachment_path=None,
    recipient_email=None,
    reply_to_email=None,
):
    subject_file = "subject.txt"
    subject = load_subject(subject_file)
    smtp_email, smtp_password = smtp_info
    smtp_server = "smtp.mail.me.com"
    port = 587
    message = MIMEMultipart()
    sendername = load_subject("sendername.txt")
    message["Subject"] = subject
    message["From"] = f"{sendername} <{smtp_email}>"
    message["To"] = recipient_email
    message.attach(MIMEText(body_text, "plain"))
    if reply_to_email:
        message.add_header("Reply-To", reply_to_email)
    if body_html:
        message.attach(MIMEText(body_html, "html"))
    if attachment_path:
        part = MIMEBase("application", "octet-stream")
        with open(attachment_path, "rb") as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        message.attach(part)
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, recipient_email, message.as_string())
        logging.info(f"Email sent successfully to {recipient_email} using {smtp_email}")
        print(f"Email sent successfully to {recipient_email} using {smtp_email}")

    except smtplib.SMTPAuthenticationError:
        logging.error(f"SMTP authentication failed for {smtp_email}")
        save_failed_smtp("failed_smtp_log.txt", smtp_info)
        print(f"SMTP authentication failed for {smtp_email}")
        with open("to_emails_failed.txt", "a") as w:
            w.write(recipient_email + "\n")
    except Exception as e:
        logging.error(
            f"Error sending email to {recipient_email} using {smtp_email}: {e}"
        )
        save_failed_email("failed_email_log.txt", recipient_email)
        print(f"Error sending email to {recipient_email} using {smtp_email}: {e}")
        with open("to_emails_failed.txt", "a") as w:
            w.write(recipient_email + "\n")


def worker(smtp_info, recipients, subject, choice, reply_to_email):
    while recipients:
        recipient_email = recipients.pop(0)
        body_text = read_file_content(get_random_file(body_folder))
        success = False
        if choice == "1":
            success = send_email(
                smtp_info,
                subject,
                body_text,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )
        elif choice == "2":
            body_html = read_file_content(get_random_file(html_folder))
            success = send_email(
                smtp_info,
                subject,
                body_text,
                body_html=body_html,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )
        elif choice == "3":
            img_path = get_random_file(img_folder)
            success = send_email(
                smtp_info,
                subject,
                body_text,
                attachment_path=img_path,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )
        elif choice == "4":
            pdf_path = get_random_file(pdf_folder)
            success = send_email(
                smtp_info,
                subject,
                body_text,
                attachment_path=pdf_path,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )
        elif choice == "5":
            body_html = read_file_content(get_random_file(html_folder))
            img_path = get_random_file(img_folder)
            success = send_email(
                smtp_info,
                subject,
                body_text,
                body_html=body_html,
                attachment_path=img_path,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )
        elif choice == "6":
            body_html = read_file_content(get_random_file(html_folder))
            pdf_path = get_random_file(pdf_folder)
            success = send_email(
                smtp_info,
                subject,
                body_text,
                body_html=body_html,
                attachment_path=pdf_path,
                recipient_email=recipient_email,
                reply_to_email=reply_to_email,
            )

        if success:
            recipients.pop(0)
            save_recipients("to_emails.txt", recipients)


def send_mail_batch(smtp_credentials, recipients, subject, choice, reply_to_email):
    threads = []
    num_credentials = len(smtp_credentials)
    for i in range(min(num_credentials, len(recipients))):
        smtp_info = smtp_credentials[i % num_credentials]
        batch_recipients = [recipients.pop(0)]
        thread = threading.Thread(
            target=worker,
            args=(smtp_info, batch_recipients, subject, choice, reply_to_email),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    data_val = auth_login()
    if data_val == True:

        smtp_credentials_file = "smtp_credentials.txt"
        recipients_file = "to_emails.txt"
        subject_file = "subject.txt"
        smtp_credentials = load_smtp_credentials(smtp_credentials_file)
        recipients = load_recipients(recipients_file)
        subject = load_subject(subject_file)

        if not smtp_credentials or not recipients or not subject:
            print("SMTP credentials, recipients list, or subject is empty. Exiting.")
            return
        print("Select the email content type:")
        print("1. Body Text Only")
        print("2. HTML Body")
        print("3. Image + Body Text")
        print("4. PDF + Body Text")
        print("5. Image + HTML Body")
        print("6. PDF + HTML Body")

        choice = input("Enter your choice (1/2/3/4/5/6): ").strip()
        sleep_time = int(input("Sleep Time (in seconds, e.g., 60): "))
        reply_to_email = open("reply_mail.txt").read().strip()
        if choice not in {"1", "2", "3", "4", "5", "6"}:
            print("Invalid choice. Exiting.")
            return

        while recipients:
            send_mail_batch(
                smtp_credentials, recipients, subject, choice, reply_to_email
            )
            save_recipients(recipients_file, recipients)
            if recipients:
                print(
                    f"Waiting for {sleep_time} seconds before starting the next batch..."
                )
                time.sleep(sleep_time)


if __name__ == "__main__":
    open("to_emails_failed.txt", "w").close()
    main()
    failed_emails = open("to_emails_failed.txt").read().splitlines()
    for i in failed_emails:
        with open("to_emails.txt", "a") as w:
            w.write(i + "\n")
