import os, smtplib, logging
from dotenv import load_dotenv

# email.py info logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Output to email.log
file_handler = logging.FileHandler('email.log')
file_handler.setLevel(logging.INFO)

# Log time, level, location & msg
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False  # Only propagate logs from this file

def send_email(subject, message):
    # Load and set env variables
    load_dotenv(override=True)
    sender        = os.getenv("EMAIL")
    recipient     = os.getenv("EMAIL")
    gmail_smtp_pw = os.getenv("GMAIL_SMTP_PW")

    # Construct email
    content = f'Subject: {subject}\nContent-Type: text/html\n\n{message}'

    try:
        # Start up SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, gmail_smtp_pw)
        logger.info("SMTP server login successful.")

        # Send email
        server.sendmail(sender, recipient, content)
        logger.info(f"Email sent to {recipient} successfully.")

    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email: {e}")

    finally:
        server.quit()
        logger.info("SMTP server connection closed.")
