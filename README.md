

# Program Overview
This project polls the [MECOP Placement Results page](https://www.mecopinc.org/events/placement) periodically. If a change is detected or something goes wrong, the script emails me. I built this while I was waiting on internship placement results from MECOP, and I didn't want to have to keep checking the page manually. MECOP is an internship co-op program, and you can read more about it  [here](https://www.mecopinc.org/about).

## File Structure
```
mecop_poller/
├── app.py                # Main script that performs the polling
├── email_sender.py       # Module that handles the sending email logic
├── requirements.txt      # List of dependencies required for the application
└── .env                  # Required environment variables for logging into MECOP and sending emails
```

## Setup
1. Clone the repository

2. Create and setup `.env` file
   - See [Setup .env File](#setup-env-file) section

3. Create a virtual environment
   - `python -m venv env`

4. Activate the virtual environment
   - Windows: `env\Scripts\activate`
   - Linux/MacOS: `source env/bin/activate`

5. Install the dependencies
   - `pip install -r requirements.txt`

6. Run the application
   - `python app.py`
   
7. Wait!

## What to Expect
Once you run `app.py`, the application will start polling the MECOP Placement Results page. You can expect to receive email notifications if there are any changes to the placement results or if an error occurs. The application will continue to run in the background, checking for updates at the specified interval. The files `mecop_poller.log` and `email.log` will be created in the root directory with logs of each scripts' activity.

## Setup .env File
An `.env` file will be needed to log into the MECOP website and send email notifications. Here is what it should look like:
```
MECOP_EMAIL="<email address of MECOP account>"
MECOP_PASSWORD="<password of MECOP account>"
EMAIL="<email address you want to send alerts from and to>"
GMAIL_SMTP_PW="<google app password associated with above email address>"
```

### Google App Password
To send emails from your Gmail account using Google's SMTP server, you need to create a Google App Password. This is a unique password that allows the application to access your Gmail account securely. To create one follow these steps:
1. Enable two step verification on the account (instructions [here](https://support.google.com/accounts/answer/185839)).
2. Visit [this link](https://myaccount.google.com/apppasswords) and create an app password. Name it whatever you want.
3. Copy the app password it gives you into the `GMAIL_SMTP_PW` field in the `.env` file