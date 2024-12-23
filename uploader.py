
# < ======================================================================================================
# < Imports
# < ======================================================================================================

import os
import logging
import mimetypes
from datetime import datetime
from googleapiclient.http import MediaFileUpload

# < ======================================================================================================
# < Functions
# < ======================================================================================================

def get_dated_folder_name() -> str:
    """Get dated folder name from current time"""
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    current_time: str = datetime.now().strftime("%H%M")
    folder_name: str = f"{current_date}_{current_time}"
    return folder_name

def should_ignore(name: str, ignored_patterns: list[str]) -> bool:
    """Determine if a file or folder should be ignored based on the ignored patterns"""
    return any(pattern.lower() in name.lower() for pattern in ignored_patterns)

def create_folder(folder_name: str, drive_service: any, parent_folder_id: str = None) -> str:
    """Create a folder on google drive"""

    file_metadata: dict[str, str] = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id is not None:
        file_metadata['parents'] = [parent_folder_id]
    folder = drive_service.files().create(body = file_metadata, fields = 'id').execute()

    identifier = folder.get('id')

    logging.info(f"Created folder on Google Drive [{folder_name} - {identifier}]")

    return identifier

def upload_file(filepath: str, drive_service: any, folder_id: str = None) -> str:
    """Upload a given file to an existing folder on Google Drive"""

    logging.info(f"Uploading file: {filepath}")

    mimetype, _ = mimetypes.guess_type(filepath)
    media = MediaFileUpload(filepath, mimetype = mimetype)
    filename = os.path.basename(filepath)
    file_metadata = {'name': os.path.basename(filename)}
    if folder_id is not None:
        file_metadata['parents'] = [folder_id]
    file = drive_service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
    return file.get('id')

def upload_folder(local_folder_path: str, drive_service: any, folder_id: str = None) -> None:
    """Upload a given folder to an existing folder on Google Drive"""

    logging.info(f"Uploading folder: {local_folder_path}")

    folder_name: str = os.path.basename(local_folder_path)
    created_folder_id: str = create_folder(folder_name, drive_service, folder_id)

    for item in os.listdir(local_folder_path):

        if should_ignore(item):
            logging.info(f"Ignoring {item} as it matches one of the patterns in IGNORED_PATTERNS")
            continue

        local_item_path = os.path.join(local_folder_path, item)

        if os.path.isdir(local_item_path):
            upload_folder(local_item_path, drive_service, created_folder_id)
        else:
            upload_file(local_item_path, drive_service, created_folder_id)

def upload_mixed(drive_service: any, filepaths: list[str], folderpaths: list[str], folder_id: str = None) -> None:
    """Create dated subfolder within folder denoted by folder_id, and upload to it using given local filepaths and folderpaths"""

    subfolder_name: str = get_dated_folder_name()
    subfolder_id: str = create_folder(subfolder_name, drive_service, folder_id)

    for folderpath in folderpaths:
        upload_folder(folderpath, drive_service, subfolder_id)

    for filepath in filepaths:
        upload_file(filepath, drive_service, subfolder_id)

    logging.info("upload_mixed ran without error")

# < ======================================================================================================
# < Execution
# < ======================================================================================================

if __name__ == "__main__":
    pass
else:
    logging.info(f"Module '{__name__}' running")