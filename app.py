import time, requests, dotenv, os, pytz
from datetime import datetime
from bs4 import BeautifulSoup
from email_sender import send_email
import logging

dotenv.load_dotenv()

LOGIN_URL = "https://www.mecopinc.org/login"
TARGET_URL = "https://www.mecopinc.org/events/placement"
EMAIL = os.getenv("MECOP_EMAIL")
PASSWORD = os.getenv("MECOP_PASSWORD")

# Div with class "well" contains "Placement results for 2025 internships will be posted on..."
DIV_SELECTOR = ".well"

logging.basicConfig(
    filename='mecop_poller.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [Line %(lineno)d] - %(message)s'
)

def login():
    """
    Login and return a session object if successful.
    """      
    logging.info("Attempting to login...")
    try:
        login_data = {
            'email': EMAIL,
            'password': PASSWORD,
        }
         
        # Create session and login
        session = requests.Session()
        response = session.post(LOGIN_URL, data=login_data)

        # Return logged in session if successful
        if response.status_code == 200:
            logging.info("Logged in successfully.")
            return session
        else:
            error_msg = f"Login Failed: {response.status_code}: {response.text}"
            logging.error(error_msg)
            return None
    except Exception as e:
        error_msg = f"Login error: {str(e)}"
        logging.error(error_msg)
        return None

def get_content(session):
    """
    Return content of page at TARGET_URL.
    """
    logging.info("Fetching page content...")
    try:
        response = session.get(TARGET_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            target_div = soup.select_one(DIV_SELECTOR)
            if target_div:
                content = target_div.get_text(strip=True)
                logging.info(f"Found target div content: '{content}'")
                return content
            else:
                error_msg = "Couldn't find the target div"
                logging.error(error_msg)
                send_email("MECOP Results!?", f"{error_msg}<br><br>Maybe the <a href='{TARGET_URL}'>placement results</a> are out!?.")
                return None
        else:
            error_msg = f"Failed to get target page. Status code: {response.status_code}"
            logging.error(error_msg)
            send_email("MECOP Results Script", f"Couldn't get the <a href='{TARGET_URL}'>target page</a>...")
            return None
    except Exception as e:
        error_msg = f"Error getting content: {str(e)}"
        logging.error(error_msg)
        send_email("MECOP Results Script", f"Error getting content: {str(e)}")
        return None

def monitor_page():
    """
    Monitors page to check for changes.
    """
    logging.info("Starting MECOP placement page monitor")

    # Loop to retry login failures
    while True:
        try:
            logging.info("Starting new monitoring cycle...")
            session = login()
            if not session:
                logging.warning("Login failed, waiting 1 hour before retry...")
                time.sleep(3600)
                logging.info("1 hour wait complete, attempting to login again...")
                continue

            prev_content = get_content(session)
            if not prev_content:
                logging.warning("Failed to get initial content, waiting 5 minutes before retry...")
                time.sleep(5 * 60)
                logging.info("5 minute wait complete, attempting to login again...")
                continue

            # Loop to check the page content
            while True:
                logging.info("Checking for content changes...")
                content = get_content(session)
                if not content:
                    logging.warning("Failed to get content, breaking loop and attempting to login again...")
                    break  # Break this inner loop to re-login
                
                if content != prev_content:
                    change_msg = "Content change detected!"
                    logging.info(change_msg)
                    send_email("MECOP Results!?", f"The div on the <a href='{TARGET_URL}'>placement page</a> has changed!!!")
                    logging.info("Change detected - exiting script")
                    return
                else:
                    logging.info("No changes detected, waiting 5 minutes before next check...")
                    time.sleep(5 * 60) # Check every 5 minutes

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(error_msg)
            logging.info("Waiting 10 minutes before retrying due to unexpected error...")
            time.sleep(10 * 60)  # Wait 10 minutes before retrying
            logging.info("10 minutes wait complete after error, restarting monitoring cycle...")

if __name__ == "__main__":
    try:
        monitor_page()
    except KeyboardInterrupt:
        logging.info("Script terminated by user")
    except Exception as e:
        logging.critical(f"Fatal error occurred: {str(e)}")
    finally:
        logging.info("Script exiting")
