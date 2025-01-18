Polls the [MECOP Placement Results page](https://www.mecopinc.org/events/placement) every `x` hours. If a change is detected or something goes wrong, the script emails me.

## Setup
1. Clone the repository

2. Create a virtual environment
   - `python -m venv env`

3. Activate the virtual environment
   - Windows: `env\Scripts\activate`
   - Linux: `source env/bin/activate`

4. Install the dependencies
   - `pip install -r requirements.txt`

5. Run the application
   - `python app.py`
   
6. Wait!

## Example .env File
A .env file will be needed to log into the MECOP website and send email notifications. Here is what it should look like:
```
MECOP_EMAIL="<email address of MECOP account>"
MECOP_PASSWORD="<password of MECOP account>"
EMAIL="<email you want to send alerts from and to>"
GMAIL_SMTP_PW="<google app password>"
```

To send emails from your gmail account using google's SMTP server, create a [Google App Password](https://myaccount.google.com/apppasswords).