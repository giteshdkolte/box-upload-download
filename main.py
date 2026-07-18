import os 
from pathlib import Path
from dotenv import load_dotenv
import logging
import argparse
from box_tasks import Box
from logger_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)
logger.info("BOX Utility Application started!")

# Load variables from .env into the environment
env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

box_vars = {
    "client_id" : os.getenv("clientID"),
    "client_secret" : os.getenv("clientSecret"),
    "enterprise_id" : os.getenv("enterpriseID"),
    "jwt_key_id" : os.getenv("publicKeyID"),
    "private_key" : os.getenv("privateKey"),
    "private_key_passphrase" : os.getenv("passphrase")
}

# If any VPN connect, provide the proxy in .env file
proxy = os.getenv("proxy")
box = Box(box_vars, proxy)

parser = argparse.ArgumentParser(
    description="Upload or download files from Box"
)

subparsers = parser.add_subparsers(
    dest="command",
    required=True
)

# ----------------------------------------------------
# Upload
# ----------------------------------------------------
upload = subparsers.add_parser(
    "upload",
    help="Upload file to Box"
)

upload.add_argument(
    "-f",
    "--folder-id",
    required=True,
    help="Destination Box folder ID"
)

upload.add_argument(
    "-p",
    "--file-path",
    required=True,
    type=Path,
    help="Local file path"
)

upload.add_argument(
    "--force",
    action="store_true",
    help="Delete existing file before uploading"
)

# ----------------------------------------------------
# Download
# ----------------------------------------------------
download = subparsers.add_parser(
    "download",
    help="Download file from Box"
)

method = download.add_mutually_exclusive_group(required=True)

method.add_argument(
    "--by-id",
    action="store_true",
    help="Download using Box file ID"
)

method.add_argument(
    "--by-name",
    action="store_true",
    help="Download using file name"
)

download.add_argument(
    "--folder-id",
    required=True,
    help="Box folder ID"
)

download.add_argument(
    "--location",
    required=True,
    type=Path,
    help="Download directory"
)

download.add_argument(
    "--file-id",
    help="Box file ID"
)

download.add_argument(
    "--file-name",
    help="Box file name"
)

args = parser.parse_args()

if args.command == "download":

    if args.by_id and not args.file_id:
        parser.error("--file-id is required with --by-id")

    if args.by_name and not args.file_name:
        parser.error("--file-name is required with --by-name")

if args.command == "upload":

    box.upload_file_to_box(
        input_file_path=args.file_path,
        folder_id=args.folder_id,
        force=args.force
    )

elif args.command == "download":
    # Create the output location of the box where the files will be downloaded
    os.makedirs(args.location, exist_ok=True)

    if args.by_id:
        box.download_file_by_id(
            file_id=args.file_id,
            output_location=args.location,
            folder_id=args.folder_id
        )

    else:
        box.download_file_by_name(
            file_name=args.file_name,
            output_location=args.location,
            folder_id=args.folder_id
        )
