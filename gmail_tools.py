import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
# LangChain
from langchain_core.tools import tool


# =========================================================
# GMAIL CONFIG
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# =========================================================
# CONNECT GMAIL
# =========================================================

def connect_gmail():
    """
    Connect to Gmail using OAuth 2.0.

    This is an internal helper function.
    It is NOT exposed to the AI agent as a tool.
    """

    creds = None

    # Nếu đã đăng nhập trước đó thì đọc token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Nếu chưa có credentials hợp lệ
    if not creds or not creds.valid:

        # Token hết hạn nhưng có refresh token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Chưa đăng nhập lần nào
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Lưu token để lần sau không cần login lại
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Tạo Gmail API service
    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service

def extract_email_body(payload):
    """
    Extract the text content from a Gmail message payload.
    Prefer text/plain over text/html.
    """

    # Trường hợp email đơn giản, body nằm ngay trong payload
    body_data = payload.get("body", {}).get("data")

    if body_data:
        return base64.urlsafe_b64decode(
            body_data
        ).decode(
            "utf-8",
            errors="ignore"
        )

    # Trường hợp email gồm nhiều phần
    parts = payload.get("parts", [])

    # Ưu tiên text/plain
    for part in parts:

        if part.get("mimeType") == "text/plain":

            data = part.get("body", {}).get("data")

            if data:
                return base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

    # Nếu không có text/plain thì tìm sâu hơn
    for part in parts:

        if part.get("parts"):

            text = extract_email_body(part)

            if text:
                return text

    # Cuối cùng thử HTML
    for part in parts:

        if part.get("mimeType") == "text/html":

            data = part.get("body", {}).get("data")

            if data:

                html = base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

                return html_to_text(html)


def html_to_text(html):
    """
    Convert HTML email content to clean plain text.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text



# =========================================================
# TOOL 1: GET LATEST EMAILS
# =========================================================

@tool
def get_latest_emails(max_results: int = 5) -> list:
    """
    Get the latest emails from the user's Gmail inbox.

    Use this tool when the user asks for recent or latest emails.

    Args:
        max_results: Number of latest emails to retrieve.

    Returns:
        A list of emails containing id, sender, subject,
        date and snippet.
    """

    service = connect_gmail()

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg["payload"].get("headers", [])

        email_data = {
            "id": message["id"],
            "from": "",
            "subject": "",
            "date": "",
            "snippet": msg.get("snippet", "")
        }

        for header in headers:

            if header["name"] == "From":
                email_data["from"] = header["value"]

            elif header["name"] == "Subject":
                email_data["subject"] = header["value"]

            elif header["name"] == "Date":
                email_data["date"] = header["value"]

        emails.append(email_data)

    return emails


# =========================================================
# TOOL 2: SEARCH EMAILS
# =========================================================

@tool
def search_emails(
    query: str,
    max_results: int = 10
) -> list:
    """
    Search emails in the user's Gmail account.

    Use this tool when the user wants to find emails matching
    a condition, such as unread emails, emails from a sender,
    or emails containing specific keywords.

    Args:
        query: Gmail search query.
        max_results: Maximum number of emails to retrieve.

    Returns:
        A list of matching emails containing id, sender,
        subject, date and snippet.
    """

    service = connect_gmail()

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg["payload"].get("headers", [])

        email_data = {
            "id": message["id"],
            "from": "",
            "subject": "",
            "date": "",
            "snippet": msg.get("snippet", "")
        }

        for header in headers:

            if header["name"] == "From":
                email_data["from"] = header["value"]

            elif header["name"] == "Subject":
                email_data["subject"] = header["value"]

            elif header["name"] == "Date":
                email_data["date"] = header["value"]

        emails.append(email_data)

    return emails



#Tool 3 Đọc gmail chi tiết

@tool
def read_email(message_id: str) -> dict:
    """
    Read the full content of a Gmail email.

    Use this tool when the user wants to know the detailed
    content of a specific email.

    Args:
        message_id: The Gmail message ID of the email to read.

    Returns:
        The email sender, subject, date, and full body.
    """

    service = connect_gmail()

    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = msg.get("payload", {})

    headers = payload.get("headers", [])

    email_data = {
        "id": message_id,
        "from": "",
        "subject": "",
        "date": "",
        "body": ""
    }

    for header in headers:

        if header["name"] == "From":
            email_data["from"] = header["value"]

        elif header["name"] == "Subject":
            email_data["subject"] = header["value"]

        elif header["name"] == "Date":
            email_data["date"] = header["value"]

    email_data["body"] = extract_email_body(payload)

    return email_data