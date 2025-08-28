import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the Government Gazette website
url = "https://governmentgazette.sa.gov.au/"

# File to store the last known issue date
last_issue_file = "last_issue.json"

# Function to extract the latest issue date from the website
def get_latest_issue_date():
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section that contains the issue date
        # You may need to adjust this selector based on actual HTML
        issue_section = soup.find("div", class_="gazette-issue")
        if issue_section:
            date_text = issue_section.get_text(strip=True)
            return date_text
        else:
            return None
    except Exception as e:
        print(f"Error fetching the website: {e}")
        return None

# Load the last known issue date
def load_last_issue_date():
    if os.path.exists(last_issue_file):
        with open(last_issue_file, 'r') as f:
            data = json.load(f)
            return data.get("last_issue_date")
    return None

# Save the new issue date
def save_new_issue_date(date):
    with open(last_issue_file, 'w') as f:
        json.dump({"last_issue_date": date}, f)

# Main logic
latest_date = get_latest_issue_date()
last_date = load_last_issue_date()

if latest_date:
    if latest_date != last_date:
        print(f"✅ New Gazette issue detected: {latest_date}")
        save_new_issue_date(latest_date)
    else:
        print(f"No new issue detected. Last known issue date: {last_date}")
else:
    print("Could not retrieve the latest issue date.")
