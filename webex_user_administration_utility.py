import requests
import csv
from datetime import datetime
import os

# Replace these variables with your actual Webex Teams API token and organization ID
access_token = os.getenv("TOKEN")

# Function to create a new user in the Webex Teams demo organization
def create_user(display_name, email):
    url = "https://api.ciscospark.com/v1/people"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "displayName": display_name,
        "emails": [email]
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("User created successfully!")
    else:
        print("Failed to create user:", response.json()["message"])


# Function to list all users from the Webex Teams demo organization
def list_users():
    url = f"https://webexapis.com/v1/people"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    users = response.json()["items"]
    return users


# Function to export users to a CSV file
def export_to_csv(users):
    with open('webex_users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Display Name', 'Email', 'Created Date', 'Site URL'])
        for user in users:
            created_date = datetime.strptime(user['created'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            try:
                site_url = user['siteUrls'][0]
            except KeyError:
                site_url = ""               
            writer.writerow([user['displayName'], user['emails'][0], created_date, site_url])


# Main function
def main():
    # create_user("test user", "test@dev.wbx.ai")
    users = list_users()
    export_to_csv(users)

if __name__ == "__main__":
    main()
