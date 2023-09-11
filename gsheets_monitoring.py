import gspread
from oauth2client.service_account import ServiceAccountCredentials

YOUR_URL = None

def write_instagram_username_to_google_sheet(username:str) -> None:
    # Authenticate using the service account credentials and Google API key
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_GSHEETS.json', scope)
    gc = gspread.authorize(credentials)

    try:
        sheet = gc.open_by_url(YOUR_URL).sheet1
        sheet.append_row([username])
        # print(sheet.get_all_values())
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

if __name__ == "__main__":
    write_instagram_username_to_google_sheet("test_username")