from box_sdk_gen import BoxClient, BoxJWTAuth, JWTConfig
from box_sdk_gen.networking.proxy_config import ProxyConfig
from box_sdk_gen.managers.search import SearchForContentType
from box_sdk_gen.managers.uploads import (
    UploadFileAttributes,
    UploadFileAttributesParentField,
)
import os
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load variables from .env into the environment
env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

# Define logger from parent
logger = logging.getLogger(__name__)

class Box():
    def __init__(self, box_vars: dict, proxy: str):
        self.box_vars = box_vars
        self.proxy = proxy
    
    def _settingProxy(self) -> ProxyConfig:
        return ProxyConfig(
            url      = self.proxy,
            username = None,   # Add if proxy requires auth
            password = None    # Add if proxy requires auth
        )

    def _creatingBoxClient(self) -> Optional[BoxClient]:
        try:
            jwt_config = JWTConfig(
                client_id = self.box_vars["client_id"],
                client_secret = self.box_vars["client_secret"],
                enterprise_id = self.box_vars["enterprise_id"],
                jwt_key_id = self.box_vars["jwt_key_id"],
                private_key = self.box_vars["private_key"],
                private_key_passphrase = self.box_vars["private_key_passphrase"]
            )
            auth = BoxJWTAuth(config=jwt_config)
            client = BoxClient(auth=auth)
            if self.proxy:
                client = client.with_proxy(self._settingProxy())
            return client
        except Exception as err:
            logger.error(f"Cannot Established BOX Client Connection: {err}")
            return None

    def download_file_by_id(self, file_id: str, output_location: str, folder_id: str) -> str:
        """
        Usage: download_file_by_id("2233205034206", "./output/sample.csv", "382425539618")
        """
        try:
            # Fetch file metadata to get its name and verify its parent folder.
            file_info = self._creatingBoxClient().files.get_file_by_id(file_id)

            # Verify the file belongs to the expected folder.
            parent_id = file_info.parent.id if file_info.parent else None
            if parent_id != folder_id:
                raise ValueError(
                    f"File '{file_info.name}' (id={file_id}) is not in folder "
                    f"id={folder_id}. Its parent folder id is {parent_id}."
                )

            file_name = file_info.name
            output_path = os.path.join(output_location, file_name)

            # Download the file content (returns a ByteStream).
            byte_stream = self._creatingBoxClient().downloads.download_file(file_id)

            with open(output_path, "wb") as f:
                for chunk in byte_stream:
                    f.write(chunk)

            logger.info(f"[DOWNLOAD BOX FILE BY FILE ID] Saved '{file_name}' → {output_path}")
            return output_path
        except Exception as err:
            logger.error(f"[DOWNLOAD BOX FILE BY FILE ID] FAILED: {err}")
            return None

    def download_file_by_name(self, file_name: str, output_location: str, folder_id: str) -> str:
        """
        Usage: download_file_by_name("sample.csv", "./output/sample.csv", "382425539618")
        """
        try:
            # List all items in the folder and find the matching file.
            items = self._creatingBoxClient().folders.get_folder_items(folder_id, limit=1000)
            matches = [
                item for item in (items.entries or [])
                if item.type == "file" and item.name == file_name
            ]

            if not matches:
                raise FileNotFoundError(
                    f"No file named '{file_name}' found in Box folder id={folder_id}."
                )
            if len(matches) > 1:
                raise ValueError(
                    f"Multiple files named '{file_name}' found in folder id={folder_id}. "
                    "Use download_file_by_id instead."
                )

            file_id = matches[0].id
            output_path = os.path.join(output_location, file_name)

            # Download the file content.
            byte_stream = self._creatingBoxClient().downloads.download_file(file_id)

            with open(output_path, "wb") as f:
                for chunk in byte_stream:
                    f.write(chunk)

            logger.info(f"[DOWNLOAD BOX FILE BY NAME] Saved '{file_name}' → {output_path}")
            return output_path
        except Exception as err:
            logger.error(f"[DOWNLOAD BOX FILE BY NAME] FAILED: {err}")
            return None

    def upload_file_to_box(self, input_file_path: str, folder_id: str, force: bool = False) -> str:
        """
        Usage:
        
        1. If we are sure each upload is unique, force flag default is False
            upload_file_to_box(client, "requirement_1212.txt", FOLDER_ID)
        2. Flag=True if there is already file present. DELETE -> LOAD
            upload_file_to_box(client, "requirement_1212.txt", FOLDER_ID, True)
        """
        try:
            file_name = Path(input_file_path).name # Preserves the original name.

            if force:
                # Check if a file with the same name already exists in the folder.
                results = self._creatingBoxClient().search.search_for_content(
                    query=f'"{file_name}"',
                    ancestor_folder_ids=[folder_id],
                    type=SearchForContentType.FILE,
                    fields=["id", "name"],
                )
                for existing_file in (results.entries or []):
                    if existing_file.name == file_name:
                        self._creatingBoxClient().files.delete_file_by_id(existing_file.id)
                        logger.info(
                            f"FORCE FLAG IS TRUE, [UPLOAD FILE TO BOX] Deleted existing '{file_name}' "
                            f"(id={existing_file.id}) before re-upload."
                        )

            with open(input_file_path, "rb") as file_stream:
                uploaded = self._creatingBoxClient().uploads.upload_file(
                    attributes=UploadFileAttributes(
                        name=file_name,
                        parent=UploadFileAttributesParentField(id=folder_id),
                    ),
                    file=file_stream,
                )

            # upload_file returns a Files object; the first entry is the new file.
            new_file = uploaded.entries[0]
            logger.info(
                f"[UPLOAD FILE TO BOX] Uploaded '{file_name}' → Box file id={new_file.id}"
            )
            return new_file.id
        except Exception as err:
            logger.error(f"[UPLOAD FILE TO BOX] FAILED: {err}")
            return None
