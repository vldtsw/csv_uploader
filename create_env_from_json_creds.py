import json

with open("credentials.json") as f:
    data = json.load(f)

with open(".env", "w") as f:
    f.write(f'GOOGLE_SHEET_API_CREDENTIALS={json.dumps(data)}')

# todo: add prompt to also add spreadsheet id to .env
# spreadsheet_id = input("Enter spreadsheet id: ")
# with open(".env", "a") as f:
#     f.write(f'GOOGLE_SHEET_API_SPREADSHEET_ID={spreadsheet_id}')
