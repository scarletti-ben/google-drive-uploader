
# < ======================================================================================================
# < Imports
# < ======================================================================================================

import json
import logging
import logging.handlers
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# < ======================================================================================================
# < Functions
# < ======================================================================================================

def generate_credentials(client_secret_path: str, scopes: list[str]) -> Credentials:
    """Function to sign in to Google and return OAuth 2.0 credentials"""  
    flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
    credentials: Credentials = flow.run_local_server(port = 8080)
    return credentials

def save_credentials(credentials: Credentials, token_path: str) -> None:
    """Save Credentials object to a a json file"""
    with open(token_path, "w") as f:
        f.write(credentials.to_json())

def load_credentials(token_path: str) -> Credentials:
    """Load credentials object from the token json file"""
    with open(token_path, "r") as f:
        token: dict = json.load(f)
    credentials: Credentials = Credentials.from_authorized_user_info(token)
    return credentials

def get_drive_service(token_path: str, client_secret_path: str, scopes: list[str]) -> any:
    """Get an authenticated Google Drive service instance using client_secrets and or token.json"""

    credentials: any = None

    try:
        logging.info("Attempting to load credentials")
        credentials: Credentials = load_credentials(token_path)  
    except Exception as e:
        logging.info(f"An error occurred attempting to load credentials from {token_path}: {e}. Skipping to authentication")
    else:
        logging.info(f"Credentials loaded from {token_path}")

    if credentials is None or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:

            request: Request = Request()

            try:
                logging.info("Attempting to refresh credentials")
                credentials.refresh(request)
            except Exception as e:
                logging.info(f"An error occurred processing credential refresh: {e}")
                quit()
            else:
                logging.info(f"Credentials refreshed successfully")

                try:
                    logging.info(f"Attempting to save credentials to {token_path}")
                    save_credentials(credentials, token_path)
                except Exception as e:
                    logging.info(f"An error occurred attempting to save credentials: {e}")
                    quit()
                else:
                    logging.info(f"Credentials saved successfully to {token_path}")

        else:

            try: 
                logging.info(f"No valid credentials available. Attempting Google OAuth Sign In to generate credentials.")
                credentials: Credentials = generate_credentials(client_secret_path, scopes)
            except Exception as e:
                logging.info(f"An error occurred attempting to generate credentials: {e}")
                quit()
            else:
                logging.info(f"Credentials successfully generated")

                try:
                    logging.info(f"Attempting to save credentials to {token_path}")
                    save_credentials(credentials, token_path)
                except Exception as e:
                    logging.info(f"An error occurred attempting to save credentials: {e}")
                    quit()
                else:
                    logging.info(f"Credentials saved successfully to {token_path}")

    else:
        try:
            logging.info(f"Credentials checks passed. Attempting to build Google Drive Resource Object")
            output: any = build('drive', 'v3', credentials = credentials)
        except Exception as e:
            logging.info(f"An error occurred attempting to build Resource object: {e}")
            quit()
        else:
            logging.info("Returning Google Drive Resource object")
            return output

# < ======================================================================================================
# < Execution
# < ======================================================================================================

if __name__ == "__main__":
    pass
else:
    logging.info(f"Module '{__name__}' running")