import csv
import os.path
from os import listdir, getcwd
from os.path import join

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

csv_files_path = "/home/zzz/PycharmProjects/Sources_to_check/export_feedback"
# Or getcwd() - current directory
google_spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")


def add_to_source_review_gsheet(spreadsheet_id, csv_file_path):
    """
    Script for importing csv feedback file from backend to
    "Sources review" sheet on Drive
    """
    
    # todo: add starting and finished
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Getting credentials from .env file
            # flow = InstalledAppFlow.from_client_secrets_file(os.getenv("GOOGLE_SHEET_API_CREDENTIALS"), SCOPES)
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # fixme: this is not working??
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    # todo: login to another function?

    try:
        if not csv_file_path:
            print("No CSV file detected.")
            return

        csv_file_name = csv_file_path.split("/")[-1]
        service = build("sheets", "v4", credentials=creds)
        sheet_metadata = (
            service.spreadsheets()
            .get(spreadsheetId=spreadsheet_id)
            .execute()
        )
        sheets = [sheet["properties"]["title"] for sheet in sheet_metadata.get("sheets", "")]
        if csv_file_name in sheets:
            # Overwriting existing data in sheet
            with open(csv_file_path, newline="") as f:
                reader = csv.reader(f)
                values = list(reader)
            response = (
                service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    valueInputOption="RAW",
                    range=csv_file_name,
                    body={"values": values},
                )
                .execute()
            )
            print(f'Sheet rewritten - {response["updatedRange"]}')
            # todo: change tab colour

        else:
            # Creating new sheet with name of the file
            body = {"requests": {"addSheet": {"properties": {"title": csv_file_name}}}}
            response = (
                service.spreadsheets()
                .batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=body
                )
                .execute()
            )
            print(f'Sheet created - {response["replies"][0]["addSheet"]["properties"]["title"]}')

            # Opening CSV feedback file and adding it's content to gsheet
            with open(csv_file_path, newline="") as f:
                reader = csv.reader(f)
                values = list(reader)
            response = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    valueInputOption="RAW",
                    range=csv_file_name,
                    body={"values": values},
                )
                .execute()
            )
            print(f'Range created - {response["updates"]["updatedRange"].split("!")[-1]}')

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    # Sorting to avoid shuffling large sources files with others from local uploading
    files = sorted(
        join(csv_files_path, file)
        for file in listdir(csv_files_path)
        if file.endswith(".csv")
    )

    for file in files:
        add_to_source_review_gsheet(
            spreadsheet_id=google_spreadsheet_id,
            csv_file_path=file
        )
