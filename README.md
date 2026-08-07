# 📦 Box Upload & Download Utility

A lightweight Python utility to **upload** and **download** files from **Box** using the **Box SDK Gen (JWT Authentication)**.

## Features

- Upload files to a Box folder
- Download files using **File ID**
- Download files using **File Name**
- Optional **force upload** (delete existing file and re-upload)
- JWT Authentication
- Optional proxy support
- Console and file logging
- Command-line interface using `argparse`

---

## Project Structure

```
.
├── main.py                 # Entry point
├── box_tasks.py            # Box operations
├── logger_config.py        # Logger configuration
├── .env                    # Environment variables
├── logs/                   # Log files
└── output/                 # Downloaded files
```

---

## Prerequisites

- Python 3.12.3
- Box Developer Application with JWT Authentication enabled
- Enterprise ID
- Client ID
- Client Secret
- Public Key ID
- Private Key
- Private Key Passphrase
- Add/Invite Platform App (Service Account) email to the folder which will be used for upload or download

## NOTE: Refer "create-box-developer-account\README.md" if BOX developer account is not present.

---

## Installation

Clone the repository

```bash
git clone https://github.com/giteshdkolte/box-upload-download.git
cd box-upload-download
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
clientID=
clientSecret=
enterpriseID=
publicKeyID=
privateKey=
passphrase=

# Optional
proxy=
```

---

# Usage

## Upload a File

Upload a file to the specified Box folder.

### Replace existing file if present

```bash
python main.py upload --folder-id 401175004617 --file-path "../box/business.csv" --force
```

### Terminal
```text
2026-07-19 00:09:59,257 | INFO     | __main__ | BOX Utility Application started!
2026-07-19 00:10:01,672 | INFO     | box_tasks | FORCE FLAG IS TRUE, [UPLOAD FILE TO BOX] Deleted existing 'business.csv' (id=2355400643132) before re-upload.
2026-07-19 00:10:04,792 | INFO     | box_tasks | [UPLOAD FILE TO BOX] Uploaded 'business.csv' → Box file id=2355400331338
```

### Upload file if not present in BOX folder (will cause error if file already present; use --force argument)

```bash
python main.py upload --folder-id 401175004617 --file-path "../box/business.csv"
```
### NOTE: This upload file to Box is tested with Free BOX account, which 1 version of the file. Please test on paid account.

### Terminal
```text
2026-07-19 00:09:52,945 | INFO     | __main__ | BOX Utility Application started!
2026-07-19 00:09:56,377 | INFO     | box_tasks | [UPLOAD FILE TO BOX] Uploaded 'business.csv' → Box file id=2355400643132
```
---

## Download by File ID

```bash
python main.py download --by-id --folder-id 401175004617 --file-id 2355286477820 --location ./output
```
### Terminal
```text
2026-07-19 00:10:13,555 | INFO     | __main__ | BOX Utility Application started!
2026-07-19 00:10:16,428 | INFO     | box_tasks | [DOWNLOAD BOX FILE BY FILE ID] Saved 'Always Max Honor-6221-1-0-1745375078.zip' → output\Always Max Honor-6221-1-0-1745375078.zip
```
---

## Download by File Name

```bash
python main.py download --by-name --folder-id 401175004617 --file-name sample.zip --location ./output
```
### Terminal
```text
2026-07-19 00:12:23,925 | INFO     | __main__ | BOX Utility Application started!
2026-07-19 00:12:26,808 | INFO     | box_tasks | [DOWNLOAD BOX FILE BY NAME] Saved 'sample.zip' → output\sample.zip
```

---

## Command Reference

### Upload

| Argument | Required | Description |
|----------|----------|-------------|
| `--folder-id` | ✅ | Box Folder ID |
| `--file-path` | ✅ | Local file path |
| `--force` | ❌ | Delete existing file before uploading |

---

### Download

| Argument | Required | Description |
|----------|----------|-------------|
| `--by-id` | One of | Download using File ID |
| `--by-name` | One of | Download using File Name |
| `--folder-id` | ✅ | Box Folder ID |
| `--location` | ✅ | Local download directory |
| `--file-id` | Required with `--by-id` | Box File ID |
| `--file-name` | Required with `--by-name` | File name in Box |

---

## Logging

Logs are written to:

- Console
- `logs/`

A new log file is generated for every execution.

Example:

```
logs/
├── log_20260719_102305.log
├── log_20260719_141550.log
```

---

## Proxy Support

If your organization requires a proxy, specify it in the `.env` file.

```env
proxy=http://proxy.company.com:8080
```

If no proxy is specified, the application connects directly.
Note: If you don't need a proxy, better not include it .env file or comment it.

## Author

**Gitesh Kolte**

GitHub: https://github.com/giteshdkolte