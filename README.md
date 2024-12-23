## Overview

This project exists primarily as a personal learning exercise and is a crude implementation of a `PyQt` application for uploading files to my `Google Drive`

It is likely that I will freeze a similar project to a single-file application in future

This project, in its current state, is linked to the Google Drive account for `guesshuu` and folder ID `1LYpYpQwnPnlK7q7DU5cEPrpmSQZMWE0k`, this folder can be moved and renamed as Google Drive folders have unique IDs

It relies primarily on API access being enabled via `Cloud Console` for a Google Drive account, and requires a downloaded `client_secret` file in `json` format. With these two steps, the script can generate `token.json`. In future runs `token.json` will be used for authentication, or you will need to reauthenticate and regenerate a valid `token.json` from `client_secret.json`. This project does not cover setting up API access or downloading the initial `client_secret.json`

In the context of a public repository `token.json`, `client_secret.json` and `app.log` are sensitive files, with write-permissions for Google Drive, or personal information, and steps have been taken to ensure they are either ommitted or heavily redacted, originals will remain in my own encrypted storage for testing purposes

If another user is testing this, ensure that you download your own `client_secret.json`, delete the placeholder `token.json` and change folder ID in `settings.json`, I am sure other changes may be needed that I have not forseen

### Features
- Select files or folders from your PC for upload
- Upload files to the Google Drive folder specified, in a subfolder named using the current system date and time
- Makes use of the `logging` module for print-style messages in an output log file `app.log`

---

## Requirements

- **Python Version**: 3.12.1
- **Dependencies**:
  - [`PyQt5`](https://pypi.org/project/PyQt5/) => `pip install PyQt5`
  - **Google Packages** => `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`
  - Dependencies not listed above can be found in `requirements.txt` => `pip install -r requirements.txt`

---

## Usage

Setup virtual environment in your terminal window **:**
-  `C:\...\directory> python -m venv venv`
-  `C:\...\directory> .\venv\Scripts\activate`
-  `(venv) C:\...\directory> pip install -r requirements.txt`

Run the script in the appropriate virtual environment **:**
- `(venv) C:\...\directory> python main.py`

---

## File Structures

The directory should have `client_secret.json` in the format
```json
{
  "installed": {
    "client_id":"ID.apps.googleusercontent.com",
    "project_id":"...",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"...",
    "redirect_uris":["http://localhost"]
  }
}
```

The directory should have `token.json` in the format, or it will be generated from `client_secret.json`
```json
{
  "token": "...", 
  "refresh_token": "...", 
  "token_uri": "https://oauth2.googleapis.com/token", 
  "client_id": "ID.apps.googleusercontent.com", 
  "client_secret": "...", 
  "scopes": ["https://www.googleapis.com/auth/drive"], 
  "universe_domain": "googleapis.com", 
  "account": "", 
  "expiry": "2024-08-23T20:22:37"
}
```

---

## Issues

It can take an age sometimes and appears to hang, especially with an expired `token.json`

---

## Tags

python, google drive, google api, client secret, token, scopes, credentials, OAuth 2.0, authentication, logging, logger, localhost, get, post, requests, PyQt5, application, google cloud, venv, virtual environments