import time, requests, dotenv, os
from bs4 import BeautifulSoup
from email_sender import send_email

dotenv.load_dotenv()

LOGIN_URL = "https://www.mecopinc.org/login"
TARGET_URL = "https://www.mecopinc.org/events/placement"
EMAIL = os.getenv("MECOP_EMAIL")
PASSWORD = os.getenv("MECOP_PASSWORD")

# Div with class "well" contains "Placement results for 2025 internships will be posted on February 15th, 2025."
DIV_SELECTOR = ".well"

def login():
    """
    Login and return a session object if successful.
    """      
    login_data = {
        'email': EMAIL,
        'password': PASSWORD,
    }
     
    # Create session and login
    session = requests.Session()
    response = session.post(LOGIN_URL, data=login_data)

    # Return logged in session if successful
    if response.status_code == 200:
        print("Logged in successfully.")
        return session
    else:
        print("Login failed:")
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        exit()

def get_content(session):
    """
    Return content of page at TARGET_URL.
    """
    response = session.get(TARGET_URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        target_div = soup.select_one(DIV_SELECTOR)
        if target_div:
            return target_div.get_text(strip=True)
        else:
            send_email("MECOP Results!?", f"Could'nt find the div.<br><br>Maybe the <a href='{TARGET_URL}'>placement results</a> are out!?.")
            exit()
    else:
        send_email("MECOP Results Script", f"Could'nt get the <a href='{TARGET_URL}'>target page</a>...")
        exit()

def monitor_page():
    """
    Monitors page to check for changes.
    """
    session = login()
    prev_content = get_content(session)

    while True:
        hours = 3 # check every 3 hours
        time.sleep(hours * 60 * 60)

        content = get_content(session)
        
        if content != prev_content:
            send_email("MECOP Results!?", f"The div on the <a href='{TARGET_URL}'>placement page</a> has changed!!!")
            break
        else:
            print("Still looking for changes...")

if __name__ == "__main__":
    monitor_page()