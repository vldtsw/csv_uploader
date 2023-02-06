import json

data = json.load(open('credentials.json'))  # path to json creds file
f = open(".env", "x")
f.write(f'GOOGLE_SHEET_API_CREDENTIALS="{data}"')
