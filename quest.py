import gspread
from google.oauth2.service_account import Credentials
import os
import json
import base64

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

spreadsheet = None

try:
    creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_B64")
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    
    if creds_b64:
        creds_info = json.loads(base64.b64decode(creds_b64).decode())
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    elif creds_json:
        creds_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    
    client = gspread.authorize(creds)
    SHEET_ID = "13obhixzF0nnBybnFT40CjdBg_ISe6UV0WjmNxyhoD34"
    spreadsheet = client.open_by_key(SHEET_ID)
    print("Spreadsheet connected!")
except Exception as e:
    print(f"Spreadsheet error: {e}")
    spreadsheet = None

def update_leaderboard(participants):
    if spreadsheet is None:
        print("Spreadsheet not available, skipping leaderboard update")
        return
    print("Connecting to sheet...")
    try:
        sheet = spreadsheet.worksheet("Leaderboard")
        print("Sheet found, clearing...")
        sheet.clear()
    except Exception as e:
        print(f"Sheet not found, creating... Error: {e}")
        sheet = spreadsheet.add_worksheet(title="Leaderboard", rows=100, cols=5)
    
    print("Adding headers...")
    sheet.append_row(["Rank", "Name", "Student ID", "Email", "Score"])
    
    sorted_participants = sorted(participants.items(), key=lambda x: x[1]["score"], reverse=True)
    
    for rank, (student_id, data) in enumerate(sorted_participants, start=1):
        print(f"Adding {data['name']} with score {data['score']}")
        sheet.append_row([rank, data["name"], student_id, data["email"], data["score"]])
    
    print("Done!")