import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ["https://www.googleapis.com/auth/drive"]
list_images = []
def get_images():
  creds = None
  if os.path.exists("modules/token.json"):
    creds = Credentials.from_authorized_user_file("modules/token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      path_to_credentials = os.path.abspath(__file__ + "/../credentials.json")
      flow = InstalledAppFlow.from_client_secrets_file(path_to_credentials, SCOPES)
      creds = flow.run_local_server(port=0)
    with open("modules/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    results = (
        service.files()
        .list(pageSize = 1000, fields = "nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    for item in items:
      if '.png' in item["name"] or '.jpg' in item["name"] or '.jpeg' in item["name"] or '.webp' in item["name"]:
        list_images.append((f"{item['name']}%{item['id']}"))
  except HttpError as error:
    print(f"An error occurred: {error}")
  return service


get_images()