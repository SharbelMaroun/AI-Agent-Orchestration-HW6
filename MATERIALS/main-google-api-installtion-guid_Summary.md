# Comprehensive Document Translation & Summary Report

**Source Document:** main-google-api-installtion-guid.pdf (18 pages)

---

--- PAGE 1 ANALYSIS ---

This is the cover page of a technical guide.

**Main Title (Hebrew):**
Integrating Google APIs
Step-by-step guide for Client and Token setup
For Gmail and Google Calendar

**Main Title (English):**
Integrating Google APIs: A Step-by-Step Guide to Client and Token Setup for Gmail & Calendar

**Author/Copyright Information:**
Dr. Yoram Segal
(c) Dr. Yoram Segal - All Rights Reserved

**Date:**
May 2026

**Footer Note (Hebrew):**
The book is written in the masculine gender for convenience and brevity only, but it is intended for all genders.

**Visual Elements:**
The page is enclosed in a simple rectangular border. The text is centered and organized into distinct blocks: the primary title in both Hebrew and English, the author attribution, the copyright notice, the date, and a disclaimer regarding gender-neutral language at the bottom.

--- PAGE 2 ANALYSIS ---

This page contains the Table of Contents for the technical guide.

**Heading:**
Table of Contents

**Table of Contents:**

| Section Number | Section Title | Page |
| :--- | :--- | :--- |
| 1 | Keywords | 4 |
| 2 | Introduction | 4 |
| 3 | Objective | 4 |
| 4 | Before You Begin | 5 |
| 5 | Step 1: Choosing the Correct Credential Type | 5 |
| 5.1 | Why Choose OAuth Client ID | 6 |
| 6 | Step 2: Starting OAuth Client Creation | 6 |
| 7 | Step 3: Accessing the Google Auth Platform | 7 |
| 7.1 | Method A: Via Google Cloud Console | 7 |
| 7.2 | Method B: Via Direct Link | 7 |
| 7.3 | Important Note | 8 |
| 8 | Step 4: Google Auth Platform Opening Screen | 8 |
| 9 | Step 5: Filling in Application Details | 9 |
| 10 | Step 6: Choosing the Application Target Audience | 9 |
| 10.1 | Why Choose External | 9 |
| 11 | Step 7: Entering Contact Email | 10 |
| 12 | Step 8: Enabling Gmail API | 10 |
| 13 | Step 9: Enabling Google Calendar API | 11 |
| 14 | Step 10: Returning to Google Auth Platform After Enabling API | 11 |
| 15 | Step 11: Getting Familiar with the Overview Screen in the New Interface | 12 |
| 16 | Step 12: Defining Precise Permissions for Data Access | 13 |
| 16.1 | Explanation of Permissions | 13 |
| 17 | Step 13: Creating an OAuth Client of Type Desktop | 13 |
| 17.1 | How the Screen Looks After Client Creation | 14 |
| 18 | Step 14: Adding a Test User | 14 |
| 19 | Step 15: Python File for Testing | 15 |
| 20 | Step 16: Installing uv and Running the Test Program | 16 |
| 20.1 | Installing uv on Windows PowerShell | 16 |
| 20.2 | Installing uv on macOS / Linux | 16 |
| 20.3 | pyproject.toml File | 17 |
| 20.4 | Execution | 17 |
| 21 | Final Checks | 17 |
| 22 | Common Issues and Quick Fixes | 18 |
| 22.1 | Error: This app isn't verified or Access blocked | 18 |
| 22.2 | Error: Authentication fails even though the Client was created | 18 |
| 22.3 | Error: The code requests old permissions | 18 |

**Footer:**
(c) Dr. Yoram Segal - All Rights Reserved | 2

--- PAGE 3 ANALYSIS ---

**Heading:**
List of Figures

**Table of Figures:**

| Figure Number | Figure Description | Page |
| :--- | :--- | :--- |
| 1 | Creating credentials - selecting OAuth client ID | 5 |
| 2 | Configure consent screen with Create OAuth client ID button | 6 |
| 3 | Google Cloud main side menu - Google Auth Platform is not visible | 6 |
| 4 | Scrolling the main menu - the item is not directly accessible | 7 |
| 5 | Get started with Google auth platform not configured yet screen | 8 |
| 6 | Audience selection - choosing between Internal and External | 9 |
| 7 | Contact Information - Email addresses field | 10 |
| 8 | Google Calendar API enabled status screen | 11 |
| 9 | Returning to Google Auth Platform - OAuth overview after enabling APIs | 12 |
| 10 | Overview screen with Create OAuth client button | 12 |

**Footer:**
3 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 4 ANALYSIS ---

**Heading:**
1 Keywords

**Content Box (Keywords):**
The following terms are listed within a bordered box:
- token.json
- credentials.json
- OAuth client ID
- OAuth 2.0
- APIs & Services
- Google Auth Platform
- Google Cloud Console
- Test users
- Scopes
- Google Calendar API
- Gmail API
- Data access
- Audience
- Branding
- Desktop application
- google-auth-oauthlib
- google-api-python-client
- uv
- Python

**Note Box:**
A highlighted box contains the following advisory note:
"Note: Due to frequent updates by Google, there may be differences between the screenshots and the interfaces shown in this guide and the actual interface. If you cannot locate specific components, it is recommended to consult an LLM (language model) for personalized guidance. It is recommended to attach a screenshot and an explanation of the desired goal to receive an accurate and relevant response for your system."

**Heading:**
2 Introduction

**Text:**
This guide consolidates all the correct, concise, and updated steps for creating an OAuth Client for a Python program that connects to Gmail and Google Calendar, including adding a Test User, downloading the client file, and running a basic test program. The instructions are adapted to the new Google Auth Platform interface, and not just to the old APIs & Services structure that appears in the original booklet.

**Heading:**
3 Objective

**Text:**
The objective is to reach a state where the Google Cloud project has all the following components:
- Gmail API enabled.
- Google Calendar API enabled.
- OAuth screen configured in the new Google Auth Platform.
- The following precise permissions defined:
 - https://www.googleapis.com/auth/gmail.modify
 - https://www.googleapis.com/auth/calendar

**Footer:**
4 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 5 ANALYSIS ---

**Top Bullet Points:**
- Create an OAuth Client of type Desktop.
- Add a Test User so that the integration works in Testing mode.
- Download the credentials.json file for Python code.

**Heading:**
4 Before Starting

**Text:**
It is necessary to work with one Google Cloud project from the beginning of the process to the end. Ensure that the correct project is selected in the top bar before any action.
In the new interface, there are two different work areas:
- APIs & Services: Used for enabling APIs such as Gmail API and Google Calendar API.
- Google Auth Platform: Used for configuring Clients, Data access, Audience, Branding, and Test users.

This is the most important point: API enabling and OAuth configuration are not performed in the same place, and therefore one must switch between them consciously.

**Heading:**
5 Step 1: Selecting the correct Credential type

**Numbered List:**
1. Enter the Google Cloud Console and check that the desired project is selected in the top bar.
2. Go to APIs & Services -> Credentials.
3. Click on Create credentials.
4. In the menu that opens, select OAuth client ID and not API key.

**Figure 1:**
A screenshot of the Google Cloud Console "Credentials" page. The "Create credentials" button has been clicked, revealing a dropdown menu with the following options:
- API key: Identifies your project using a simple API key to check quota and access.
- OAuth client ID: Requests user consent so that your app can access the user's data.
- Service account: Enables server-to-server, app-level authentication using robot accounts.
- Help me choose: Asks a few questions to help you decide which type of credential to use.

**Figure Caption:**
Figure 1: Creating credentials - selecting OAuth client ID

**Footer:**
5 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 6 ANALYSIS ---

**Heading:**
5.1 Why choose OAuth client ID

**Text:**
The OAuth client ID credential type is required when a program needs to connect to a Gmail or Google Calendar account of a real user and obtain permission via a consent screen. An API key is not suitable for this purpose.

**Heading:**
6 Step 2: Starting the creation of the OAuth Client

**Numbered List:**
1. After selecting OAuth client ID, the Create OAuth client ID screen will open.
2. If Google displays a message that you must first configure the consent screen, click on Configure consent screen.

**Figure 2:**
A screenshot of the Google Cloud Console "Create OAuth client ID" page. The interface shows a warning box stating: "To create an OAuth client ID, you must first configure your consent screen," accompanied by a button labeled "Configure consent screen." The sidebar highlights "Clients" under the "Google Auth Platform" section.

**Figure Caption:**
Figure 2: Create OAuth client ID screen with the Configure consent screen button.

**Heading:**
7 Step 3: Entering the Google Auth Platform

**Text:**
There are two quick ways to reach the Google Auth Platform:

**Footer:**
6 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 7 ANALYSIS ---

**Heading:**
7.1 Method A: From the Google Cloud Console

**Numbered List:**
1. Open the main side menu of Google Cloud.
2. If "Google Auth Platform" appears in the list or in the area of recently used items, click on it.

**Figure 3:**
A screenshot of the Google Cloud Console side navigation menu. The menu displays various services including Marketplace, APIs and services, Agent Platform, Compute Engine, Kubernetes Engine, Cloud Storage, Security, BigQuery, Monitoring, Cloud Run, VPC network, Databases, Cloud SQL, and Google Maps Platform. A sub-menu for "Security Command Centre" is expanded, showing options like Overview, Graph search, Issues, Findings, Assets, Compliance, Posture management, Rules, Sources, Google SecOps, Fraud Defense, Model armour, Web Security Scanner, Cyber insurance hub, Binary Authorisation, Advisory notifications, Access Approval, and Managed Microsoft AD.

**Figure Caption:**
Figure 3: The Google Cloud main side menu - Google Auth Platform is not easily visible.

**Heading:**
7.2 Method B: Direct Link

**Text:**
If "Google Auth Platform" does not appear in the menu, manually open the following address in your browser, with your project ID:

**Code Block:**
https://console.cloud.google.com/auth/platform/overview?project=YOUR_PROJECT_ID

**Footer:**
7 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 8 ANALYSIS ---

**Heading:**
7.3 Important Note

**Text:**
During the actual work process, the main Google Cloud menu might not display "Google Auth Platform" clearly. In such a case, do not waste time searching the menu; the fastest and most accurate way is to use the direct link.

**Figure 4:**
A screenshot showing the "Clients" section within the Google Auth Platform interface. The table lists an OAuth 2.0 Client ID named "desktop client for gmail and calendar," created on 16 May 2024, with a specific Client ID string.

**Figure Caption:**
Figure 4: Continuing in the main menu - the item is still not directly accessible.

**Heading:**
8 Step 4: Opening the Google Auth Platform screen

**Text:**
If this is your first time accessing the Google Auth Platform for the project, the "Google auth platform not configured yet" screen will appear with a "Get started" button.

**Numbered List:**
1. Click on "Get started."
2. Afterward, the wizard for configuring "Branding" and "Audience" will begin.

**Figure 5:**
A screenshot of the Google Cloud Console showing the "Google auth platform not configured yet" landing page. The center of the screen features an illustration of a cloud icon inside a frame, with the text: "Google auth platform not configured yet. Get started with configuring your application's identity and manage credentials for calling Google APIs and Sign in with Google." Below this text is a blue button labeled "Get started."

**Figure Caption:**
Figure 5: Google auth platform not configured yet screen with the Get started button.

**Footer:**
8 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 9 ANALYSIS ---

**Heading:**
9 Step 5: Filling in Application Details

**Text:**
In the App Information screen, you must fill in the basic application details.
1. In the App name field, write a clear name, for example: gmail-calendar-test.
2. In the User support email field, select your Gmail address.
3. Click Next.

If the first screen is completed and you are at the next step, simply continue according to the instructions below.

**Heading:**
10 Step 6: Choosing the Application Audience

**Text:**
In the Audience screen, you must choose who will be able to use the application.
1. Select External.
2. Do not select Internal, unless it is a Google Workspace organization managed by an organization.
3. Click Next.

**Figure 6:**
A screenshot of the Google Cloud Console "Project configuration" page. The interface shows a progress indicator with two steps: "1. App Information" (marked with a blue checkmark) and "2. Audience." Under the Audience section, there are two radio button options:
* Internal: "Only available to users within your organisation. You will not need to submit your app for verification."
* External: "Available to any test user with a Google Account. Your app will start in testing mode and will only be available to users that you add to the list of test users. Once your app is ready to push to production, you may need to verify your app."
A "Next" button is visible at the bottom left.

**Figure Caption:**
Figure 6: Audience screen - choosing between Internal and External.

**Heading:**
10.1 Why choose External

**Text:**
For a regular Gmail account or a local testing project, External is the correct path, as it allows working in Testing mode with a list of Test users.

**Footer:**
9 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 10 ANALYSIS ---

**Heading:**
11 Step 7: Entering Contact Information

**Text:**
In the Contact Information screen, you must enter the email address that will receive updates from Google.
1. In the Email addresses field, enter your email address.
2. Click Next.
3. On the next screen, click Create.

**Figure 7:**
A screenshot of the Google Cloud Console "Project configuration" page. The interface shows a progress indicator with four steps: "1. App Information" (checked), "2. Audience" (checked), "3. Contact Information" (active), and "4. Finish." Under the "Contact Information" section, there is an input field labeled "Email addresses *" with a sub-text: "These email addresses are for Google to notify you about any changes to your project." A "Next" button is located below the input field.

**Figure Caption:**
Figure 7: Contact Information screen - Email addresses field.

**Heading:**
12 Step 8: Enabling Gmail API

**Text:**
1. Return to the Google Cloud Console and verify that the correct project is selected.
2. Open the main left-hand menu.
3. Select APIs & Services.
4. In the sub-menu, select Library.
5. In the search field, type Gmail API.
6. Click on the Gmail API result.
7. Click on Enable.

If the Gmail API is already enabled, no further action is required.

**Footer:**
10 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 11 ANALYSIS ---

**Heading:**
13 Step 9: Enabling Google Calendar API

**Text:**
1. Stay in the Google Cloud Console.
2. Go again to APIs & Services -> Library.
3. In the search field, type Google Calendar API.
4. Click on the Google Calendar API result.
5. Click on Enable.

**Figure 8:**
A screenshot of the Google Cloud Console "API/Service details" page for the "Google Calendar API." The interface confirms the status is "Enabled." The page displays service information, documentation links (Overview, Quickstarts, API reference), and tabs for Metrics, Quotas and system limits, and Credentials.

**Figure Caption:**
Figure 8: Google Calendar API screen in Enabled status.

**Text:**
The system requires enabling both the Gmail API and the Calendar API, as without enabling the API, it is impossible to perform application calls even if the OAuth is configured correctly.

**Heading:**
14 Step 10: Returning to Google Auth Platform after API Enablement

**Text:**
After enabling the Google Calendar API, you might remain on the API/Service screen and not see a clear way to return to the Google Auth Platform.
In this case:
1. There is no need to search in the menu.
2. Open the following link directly:

`https://console.cloud.google.com/auth/platform/overview?project=YOUR_PROJECT_ID`

3. Ensure that you return to the screen where the left-hand menu appears.

**Footer:**
11 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 12 ANALYSIS ---

**List of Navigation Items:**
* Overview
* Branding
* Audience
* Clients
* Data access
* Verification centre
* Settings

**Figure 9:**
A screenshot of the Google Cloud Console "OAuth overview" page. The left-hand sidebar lists the navigation items mentioned above. The main content area displays a "Metrics" section stating "You haven't configured any OAuth clients for this project yet" with a "Create OAuth client" button, and a "Project checkup" section stating "No project health recommendations found for your project."

**Figure Caption 9:**
Figure 9: Returning to the OAuth overview in the Google Auth Platform after enabling APIs.

**Heading:**
15 Step 11: Getting to know the Overview screen in the new interface

**Text:**
In the Overview screen of the Google Auth Platform, you can verify that the project is in the correct place. If a Client has not yet been created, or if a Client has already been created, it will appear along the way.

**Figure 10:**
A screenshot identical to Figure 9, showing the "OAuth overview" page within the Google Cloud Console, highlighting the "Metrics" section and the "Create OAuth client" button.

**Figure Caption 10:**
Figure 10: Overview screen with the Create OAuth client button.

**Text:**
If you see the "Create OAuth client" button, it means you are in the correct place in the new interface.

**Footer:**
12 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 13 ANALYSIS ---

**Heading:**
16 Step 12: Defining precise permissions in Data access

**Text:**
In this step, we define the Scopes in practice. In the new interface, we do not look for the old OAuth consent screen, but rather work through Data access within the Google Auth Platform.
1. Click on Data access in the left menu.
2. Click on Add or Remove Scopes.
3. In the "Manually add scopes" area, add the following two permissions:

`https://www.googleapis.com/auth/gmail.modify`
`https://www.googleapis.com/auth/calendar`

4. Click on "Add to table".
5. Verify that these two permissions appear in the list.
6. Click on "Save" or "Update" according to what appears on the screen.

**Heading:**
16.1 Explanation of permissions

**Table 1: Explanation of required permissions**

| Permission | Meaning |
| :--- | :--- |
| gmail.modify | Reading, searching, tagging, changing status, creating drafts, and sending/managing messages at the Gmail API level. |
| calendar | Full access to the main calendar and appointments, including creating, updating, and deleting events. |

**Heading:**
17 Step 13: Creating an OAuth Client of type Desktop

**Text:**
1. Click on Clients in the left menu.
2. Click on "Create OAuth client" or "Create client".
3. In the "Application type" field, select "Desktop" or "Desktop app".
4. In the "Name" field, type a clear name, for example:

**Footer:**
13 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 14 ANALYSIS ---

**Text Box:**
`desktop-client-for-gmail-and-calendar`

**Text:**
5. Click "Create".
6. After the client is created, click "Download JSON" and save the file to your computer.
7. Rename the file to `credentials.json` inside your project folder.

**Heading:**
17.1 How the screen looks after client creation

**Text:**
After creating the client, the "Clients" list should show a row with:
- Name: `desktop-client-for-gmail-and-calendar`
- Creation date: [Date of creation]
- Type: Desktop
- Client ID: A unique identifier approximately 72 characters long

Note: No screenshot is required for this step. When performing this step, ensure that the row appears in the "Clients" list before moving to the next step.

**Heading:**
18 Step 14: Adding a Test user

**Text:**
When the application is in "Testing" mode, only users appearing in the "Test users" list will be able to connect and receive a token.

1. From the Google Auth Platform, click on "Audience" in the left menu.
2. Scroll to the "Test users" area.
3. Click on "Add users".
4. In the window that opens, type the Gmail address from which the connection will actually be performed.
5. If required, you can add several additional addresses for testing.
6. Click "Save".
7. Verify that the address now appears in the "Test users" list.

**Footer:**
14 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 15 ANALYSIS ---

**Heading:**
19 Step 15: Testing file

**Text:**
Below is a minimal test program that creates a draft in Gmail and an event in the main calendar for 4 hours from now. The code matches the settings defined in this guide.

**Code Block:**
```python
from __future__ import annotations

import base64
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
 "https://www.googleapis.com/auth/gmail.modify",
 "https://www.googleapis.com/auth/calendar",
]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

def get_credentials -> Credentials:
 creds = None
 if Path(TOKEN_FILE).exists:
 creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

 if not creds or not creds.valid:
 if creds and creds.expired and creds.refresh_token:
 creds.refresh(Request)
 else:
 flow = InstalledAppFlow.from_client_secrets_file(
 CREDENTIALS_FILE, SCOPES)
 creds = flow.run_local_server(port=0)
 Path(TOKEN_FILE).write_text(creds.to_json, encoding="utf-8")
 return creds

def create_gmail_draft(gmail_service):
 msg = EmailMessage
 msg["To"] = "me"
 msg["Subject"] = "Test draft from Python"
 msg.set_content("This is a minimal test draft created by Python.")
 raw = base64.urlsafe_b64encode(msg.as_bytes).decode
 draft = gmail_service.users.drafts.create(
 userId="me",
 body={"message": {"raw": raw}},
 ).execute
 return draft["id"]

def create_calendar_event(calendar_service):
 start = datetime.now.astimezone + timedelta(hours=4)
```

**Footer:**
15 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 16 ANALYSIS ---

**Code Block (Continuation from Page 15):**
```python
 end = start + timedelta(hours=1)
 event = {
 "summary": "Python API test event",
 "description": "Minimal test event created by Python.",
 "start": {"dateTime": start.isoformat},
 "end": {"dateTime": end.isoformat},
 }
 created = calendar_service.events.insert(
 calendarId="primary",
 body=event,
 ).execute
 return created["id"], created.get("htmlLink")

def main:
 creds = get_credentials
 gmail_service = build("gmail", "v1", credentials=creds)
 calendar_service = build("calendar", "v3", credentials=creds)

 draft_id = create_gmail_draft(gmail_service)
 event_id, event_link = create_calendar_event(calendar_service)

 print(f"Draft created: {draft_id}")
 print(f"Calendar event created: {event_id}")
 print(f"Event link: {event_link}")

if __name__ == "__main__":
 main
```

**Heading:**
20 Step 16: Installing uv and running the test program

**Heading:**
20.1 Installing uv on Windows PowerShell

**Code Block:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Heading:**
20.2 Installing uv on macOS / Linux

**Code Block:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Text:**
After installation, open a new terminal and check:

**Code Block:**
```bash
uv --version
```

**Footer:**
16 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 17 ANALYSIS ---

**Heading:**
20.3 pyproject.toml file

**Code Block:**
```toml
[project]
name = "gmail-calendar-test"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
 "google-api-python-client",
 "google-auth-oauthlib",
 "google-auth-httplib2",
]
```

**Heading:**
20.4 Execution

**Numbered List:**
1. Create a new folder for the project.
2. Save main.py in it.
3. Save pyproject.toml in it.
4. Copy the credentials.json file downloaded from Google Auth Platform into it.
5. Open a terminal inside the folder and run:

**Code Block:**
```bash
uv sync
uv run main.py
```

**Text:**
During the first run, a browser will open to authenticate with the Google account, and after approval, a local token.json file will be created to be used for subsequent runs.

**Heading:**
21 Final Checks

**Text:**
After running the program, you should verify the following four results:
1. The Google permission screen appears in the browser without an access error.
2. A new draft is created in the Gmail inbox under Drafts.
3. A new event is created in the main calendar starting 4 hours from the time of execution.
4. A token.json file is created in the project folder.

**Footer:**
17 | (c) Dr. Yoram Segal - All Rights Reserved

--- PAGE 18 ANALYSIS ---

**Heading:**
22 Common Issues and Quick Fixes

**Heading:**
22.1 Error: "This app isn't verified" or "Access blocked"

**Text:**
If the application is in "Testing" mode, this is a normal warning screen. As long as the connected account is listed under "Test users," you can continue the process.

**Heading:**
22.2 Error: Connection fails despite Client being created

**Text:**
Ensure the following three items are verified:
- The connected account is added under "Test users" in the "Audience" section.
- The Scopes are defined under "Data access."
- Both "Gmail API" and "Google Calendar API" are enabled under "APIs & Services" -> "Library."

**Heading:**
22.3 Error: The code requests old permissions

**Text:**
If you previously defined different Scopes, you must delete the "token.json" file and run the program again to force a new OAuth process with the updated permissions.

**Footer:**
18 | (c) Dr. Yoram Segal - All Rights Reserved

---

## Cross-Reference Clarifications

- **Page 2 → Page 4:** The Table of Contents references section 1 (Keywords) and section 3 (Objective), which are detailed on page 4.
- **Page 2 → Page 5:** The Table of Contents references section 4 (Before You Begin) and section 5 (Step 1), which are detailed on page 5.
- **Page 2 → Page 6:** The Table of Contents references section 5.1 (Why Choose OAuth Client ID) and section 6 (Step 2), which are detailed on page 6.
- **Page 2 → Page 7:** The Table of Contents references section 7 (Step 3) and its subsections, which are detailed on page 7.
- **Page 2 → Page 8:** The Table of Contents references section 7.3 (Important Note) and section 8 (Step 4), which are detailed on page 8.
- **Page 2 → Page 9:** The Table of Contents references section 9 (Step 5) and section 10 (Step 6), which are detailed on page 9.
- **Page 2 → Page 10:** The Table of Contents references section 11 (Step 7) and section 12 (Step 8), which are detailed on page 10.
- **Page 2 → Page 11:** The Table of Contents references section 13 (Step 9) and section 14 (Step 10), which are detailed on page 11.
- **Page 2 → Page 12:** The Table of Contents references section 15 (Step 11), which is detailed on page 12.
- **Page 2 → Page 13:** The Table of Contents references section 16 (Step 12) and section 17 (Step 13), which are detailed on page 13.
- **Page 2 → Page 14:** The Table of Contents references section 17.1 (How the Screen Looks) and section 18 (Step 14), which are detailed on page 14.
- **Page 2 → Page 15:** The Table of Contents references section 19 (Step 15), which is detailed on page 15.
- **Page 2 → Page 16:** The Table of Contents references section 20 (Step 16) and its subsections, which are detailed on page 16.
- **Page 2 → Page 17:** The Table of Contents references section 20.3, 20.4, and 21, which are detailed on page 17.
- **Page 2 → Page 18:** The Table of Contents references section 22 (Common Issues), which is detailed on page 18.
- **Page 3 → Page 5:** The List of Figures references Figure 1, which is located on page 5.
- **Page 3 → Page 6:** The List of Figures references Figures 2 and 3, which are located on page 6.
- **Page 3 → Page 7:** The List of Figures references Figure 4, which is located on page 7.
- **Page 3 → Page 8:** The List of Figures references Figure 5, which is located on page 8.
- **Page 3 → Page 9:** The List of Figures references Figure 6, which is located on page 9.
- **Page 3 → Page 10:** The List of Figures references Figure 7, which is located on page 10.
- **Page 3 → Page 11:** The List of Figures references Figure 8, which is located on page 11.
- **Page 3 → Page 12:** The List of Figures references Figures 9 and 10, which are located on page 12.
- **Page 11 → Page 12:** The text instructs the user to return to the Google Auth Platform overview screen, which is depicted on page 12.
- **Page 14 → Page 15:** The text mentions moving to the next step, which is the Python testing file located on page 15.
- **Page 16 → Page 17:** The text references the pyproject.toml file, which is provided on page 17.
- **Page 18 → Page 13:** The troubleshooting section references defining Scopes under "Data access," which is explained on page 13.
- **Page 18 → Page 14:** The troubleshooting section references adding users to the "Test users" list, which is explained on page 14.
