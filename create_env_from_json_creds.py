import json

with open("credentials.json") as f:
    data = json.load(f)

with open(".env", "w") as f:
    f.write(f'GOOGLE_SHEET_API_CREDENTIALS={json.dumps(data)}')
