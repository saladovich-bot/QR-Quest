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
    if creds_b64:
        creds_info = json.loads(base64.b64decode(creds_b64).decode())
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


def load_participants_from_sheets():
    if spreadsheet is None:
        return {}
    try:
        sheet = spreadsheet.worksheet("Participants")
        rows = sheet.get_all_records()
        participants = {}
        for row in rows:
            student_id = str(row["student_id"])
            participants[student_id] = {
                "name": row["name"],
                "email": row["email"],
                "score": int(row["score"]),
                "answers": json.loads(row["answers"])
            }
        print(f"Loaded {len(participants)} participants from Sheets")
        return participants
    except Exception as e:
        print(f"Error loading participants: {e}")
        return {}


def save_participant_to_sheets(student_id, data):
    if spreadsheet is None:
        return
    try:
        sheet = spreadsheet.worksheet("Participants")
        rows = sheet.get_all_records()
        
        # البحث عن الصف الموجود
        for i, row in enumerate(rows, start=2):
            if str(row["student_id"]) == str(student_id):
                sheet.update(f"A{i}:E{i}", [[
                    student_id,
                    data["name"],
                    data["email"],
                    data["score"],
                    json.dumps(data["answers"])
                ]])
                return
        
        # إذا مو موجود، أضف صف جديد
        if len(rows) == 0:
            sheet.append_row(["student_id", "name", "email", "score", "answers"])
        
        sheet.append_row([
            student_id,
            data["name"],
            data["email"],
            data["score"],
            json.dumps(data["answers"])
        ])
    except Exception as e:
        print(f"Error saving participant: {e}")


def update_leaderboard(participants):
    if spreadsheet is None:
        return
    try:
        sheet = spreadsheet.worksheet("Leaderboard")
        sheet.clear()
    except:
        sheet = spreadsheet.add_worksheet(title="Leaderboard", rows=100, cols=5)
    
    sheet.append_row(["Rank", "Name", "Student ID", "Email", "Score"])
    sorted_participants = sorted(participants.items(), key=lambda x: x[1]["score"], reverse=True)
    for rank, (student_id, data) in enumerate(sorted_participants, start=1):
        sheet.append_row([rank, data["name"], student_id, data["email"], data["score"]])
    print("Leaderboard updated!")