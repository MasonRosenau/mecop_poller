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

# Div with class "well" contains "Placement results for 2025 internships will be posted on February 15th, 2025."
DIV_SELECTOR = ".well"

logging.basicConfig(
    filename='mecop_poller.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def login():
    """
    Login and return a session object if successful.
    """      
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
            send_email("MECOP Results!?", f"{error_msg}<br><br>Maybe the <a href='{TARGET_URL}'>placement results</a> are out!?.")
            return None
    except Exception as e:
        error_msg = f"Login error: {str(e)}"
        logging.error(error_msg)
        send_email("MECOP Results!?", f"{error_msg}<br><br>Maybe the <a href='{TARGET_URL}'>placement results</a> are out!?.")
        return None

def get_content(session):
    """
    Return content of page at TARGET_URL.
    """
    try:
        response = session.get(TARGET_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            target_div = soup.select_one(DIV_SELECTOR)
            if target_div:
                return target_div.get_text(strip=True)
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
            session = login()
            if not session:
                logging.warning("Login failed, retrying in 1 hour...")
                time.sleep(3600)
                continue

            prev_content = get_content(session)
            if not prev_content:
                logging.warning("Failed to get initial content, retrying in 1 hour...")
                time.sleep(3600)
                continue

            # Loop to check the page content
            while True:
                content = get_content(session)
                if not content:
                    logging.warning("Failed to get content, breaking to re-login")
                    break  # Break this inner loop to re-login
                
                if content != prev_content:
                    change_msg = "Content change detected!"
                    logging.info(change_msg)
                    send_email("MECOP Results!?", f"The div on the <a href='{TARGET_URL}'>placement page</a> has changed!!!")
                    return
                else:
                    logging.info("Still looking for changes...")
                    time.sleep(3 * 60 * 60) # Check every 3 hours

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(error_msg)
            time.sleep(3600)  # Wait 1 hour before retrying

if __name__ == "__main__":
    monitor_page()
