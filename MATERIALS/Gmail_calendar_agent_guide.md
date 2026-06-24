# Connecting an AI Agent to Gmail & Google Calendar — Full Guide

*Based on Dr. Yoram Segal's two-part walkthrough. Covers the Google Cloud setup (Video 1), the Python test code via an AI coding agent (Video 2), the concepts behind each step, and what you still need to build for the graded assignment.*

---

## 1. The Goal

Give your **AI agent its own keys to a Google account** so it can act on real data instead of only chatting. By the end of both videos, your Python code can:

- **Read Gmail** — scan the inbox, pull out emails, understand their content.
- **Write to Gmail** — create drafts / send mail.
- **Write to Google Calendar** — create events automatically.

The entire Google Cloud Console dance exists to produce **two files**:

| File | What it is | Created in |
|------|-----------|-----------|
| `client_secret.json` (the **client**) | Your app's *identity* — identifies your program to Google. Does **not** by itself grant access to any data. | Video 1 |
| `token.json` (the **token**) | The actual access grant — produced *after* a user consents. This is what lets the code call Gmail/Calendar as you. | Video 2 (first run) |

> **Key mental model:** `client secret → user consent → token → API calls`. Video 1 makes the client. Video 2 turns it into a token and proves it works.

---

## 2. The Assignment (the real deliverable)

The credential setup is just plumbing. The graded task is:

> Build an **AI agent** that reads incoming emails, finds a **meeting invitation**, and **adds that meeting to Google Calendar** — then sends a **completion email to the lecturer** when the full game finishes.

**Submission address:**

```
rmisegal+uoh26b@gmail.com
```

### Why that exact address matters

It uses Gmail **plus-addressing**. Everything before the `+` is the real mailbox (`rmisegal@gmail.com`); everything after (`uoh26b`) is an arbitrary tag Gmail ignores for delivery but keeps visible. This lets the lecturer:

- Receive every student's submission in **one inbox**.
- **Auto-filter and label** all `+uoh26b` mail into a single folder (the label/filter trick he demos at the end of Video 1 is the *receiving* side of this).

**→ Send to the address exactly as written, tag and all. Do not "clean it" to `rmisegal@gmail.com`** or it bypasses his filter and may not get counted.

---

## 3. Core Concepts (worth understanding before you build)

### Client vs. Token
- **Client** = the app's identity. Safe-ish to lose on its own — it can't touch any mailbox until a user consents.
- **Token** = the access grant tied to a specific consenting user. This is the sensitive runtime artifact.
- **Both are stored together in a folder OUTSIDE your project** (not inside `007/`).

### Scopes (permissions / הרשאות)
Scopes define *what* you allow the app to do (read mail, send mail, edit calendar, etc.). In `Data Access → Add/Remove Scopes` you add them one per line.
- Segal admits that on a throwaway free account he sometimes grants **all** scopes for convenience — and explicitly warns this is **bad practice**, never to be done in a professional system.
- The correct approach: add **only the specific scopes you need** (one Gmail scope + one Calendar scope in the demo).

### Test Users
Because the app is **External** and **unverified**, Google only lets **designated test users** complete the consent flow (up to 100). The Gmail account you actually authenticate with in Video 2 **must** be on this list, or consent fails.

### `uv` (the Python environment in Video 2)
`uv` is a fast virtual-environment / package manager. Segal uses it because Google's client libraries update constantly; `uv` isolates the project and handles version churn automatically, so you're not chasing dependency updates by hand.

---

## 4. VIDEO 1 — Creating the Google Client

Tool: **Google Cloud Console** (free; ignore the $300 credit prompt).

### Step-by-step

1. **Sign in** to the free Gmail account you'll use.
2. Open the **Google Cloud Console**.
3. **Create a New Project.**
   - Name it after your team. Example: `army_007`.
   - Use **snake_case, lowercase, no spaces** to avoid headaches later.
4. **Enable the Gmail API:** search "Gmail API" → select it → **Enable**.
5. **Create credentials:** `Credentials → Create Credentials → OAuth client ID` ("option 2").
6. **Configure the OAuth consent / Branding screen:**
   - App name the end-user sees — add a unique number so it's not a duplicate.
   - Support email = your email.
   - User type = **External**.
   - Operate as a **Test User** (this is a private/personal use case, not an org).
   - Developer contact = your email (you can comma-separate several).
   - Agree → **Create**.
7. **Enable the Google Calendar API:** hamburger menu → `APIs & Services → Library` → search "Google Calendar API" → **Enable**.
   - *(Same pattern works later for Drive, Translate, YouTube, etc. — all on the same client.)*
8. **Set scopes:** `Data Access → Add/Remove Scopes` → add the **Gmail scope** and **Calendar scope** (one per line) → **Update**.
9. **Create the client:** `Clients → Create Client` → choose **Desktop app** (not mobile/Chrome/TV — it runs from the terminal/CLI) → name it → **Create**.
10. **Download the client JSON** — *the most important step.*
    - Save it in a **secret folder OUTSIDE your project**.
    - Rename to something simple, e.g. `my_google_safe.json`.
11. **Add test users:** `Audience → Test Users → Add Users`.
    - Add your project Gmail **and** your teammates' personal emails (up to 100) so everyone can authenticate.
    - All mail/calendar data lives on the main account; the listed emails are people allowed to *run software* against that account.
12. **(Optional convenience)** In Gmail, create a **label** for testing — e.g. `bio`, prefixed with `0-` so it sorts to the top.

**Output of Video 1:** `client_secret.json` saved in an external secret folder, with two APIs enabled and the right scopes + test users configured.

---

## 5. VIDEO 2 — Python Code That Uses the Client

Tool for writing code: an **AI coding agent in the terminal**. Segal uses **Codex** (OpenAI's CLI agent) and notes it currently gives more freedom of action for this kind of terminal task — while acknowledging Claude has its own strong advantages. **The principle matters more than the tool**: Claude, Gemini, or whatever you already use works the same way.

### Setup
1. Log into the Gmail account you registered as a **test user** in Video 1. *(This is the critical link — wrong account = consent fails.)*
2. Create a project folder for the code, e.g. `007/`, and `cd` into it.
3. Keep **client + token in the external folder**, *not* inside `007/`.

### The prompt given to the AI agent (paraphrased)
> I've set up a Google API client that connects to Gmail and Calendar; it's in `<external folder path>`. The **token** that gets created must be saved in the **same folder as the client**. Build a Python **test program** in the current project that **writes an email into Gmail Drafts** and **adds a Calendar event for today, 4 hours from now**. It must run under **`uv`**, so install `uv` too, and give me the **run command**.

### What the AI agent does autonomously
- Installs `uv`; checks Python version and git.
- Generates the test program (~141 lines; includes a **README** — "no code without a README").
- Creates the `uv` config (`pyproject.toml`) pinning the needed library versions.
- Sets up an **environment variable** so the program can locate the client + token files regardless of where it's run from.

### Running it
1. **First run** → no token yet → the browser opens → log in and **approve the scopes** as the test user → "you may close this window."
2. A **`token.json`** now appears in the secret folder next to the client.
3. **Second run** (token now exists) → no browser prompt → the program:
   - Adds a **Calendar event**, and
   - Creates an **email draft** in Gmail.
4. Verify by refreshing Gmail Drafts and Calendar — both entries appear, created entirely by the Python code.

**Output of Video 2:** a working `token.json` and proof that the same credential drives both Gmail (draft) and Calendar (event).

---

## 6. The Full Picture

```
VIDEO 1                          VIDEO 2
─────────                        ─────────
Cloud project                    Log in as test user
   │                                │
Enable Gmail API                 AI agent writes Python (uv)
Enable Calendar API                 │
   │                             1st run → browser consent
Create OAuth client                 │
   │                             token.json created
Set scopes (Gmail+Calendar)         │
   │                             2nd run →
Download client_secret.json         ├── draft added to Gmail
   │                                └── event added to Calendar
Add test users
   │
(Gmail label for testing)

           client → consent → token → API calls
```

---

## 7. Gap Between the Demo and Your Assignment

The demo does **less** than the graded task. Plan for the difference:

| Demo (Video 2) | Assignment |
|----------------|-----------|
| Creates a **draft** | Must actually **send** an email |
| Adds a **fixed** event (4h out) | Must **read a real email**, **extract** the meeting time, and add *that* event |
| Gmail write only | Needs Gmail **read** scope **and** **send** scope exercised |
| No parsing | Needs a **parsing/extraction** step to find the meeting in the email text |

So your agent needs roughly these reusable tools:
- `read_emails()` — pull inbox messages.
- `extract_meeting()` — find a meeting invite + its time in an email.
- `add_calendar_event()` — book the extracted meeting.
- `send_email()` — send the completion email to `rmisegal+uoh26b@gmail.com`.

You may send the test email **from yourself to yourself**, or from an external account, then confirm the message arrived and the event was added.

---

## 8. Gotchas & Troubleshooting

- **Token expiry** — the token expires periodically. *This is the thing most likely to bite you at the deadline.* If you test now, leave it a few days, then run for final submission, expect possible re-auth. Build the recovery path in from the start: **delete `token.json` → next run reopens the browser → re-consent.**
- **Wrong account at consent** — you must authenticate with a Gmail that's in the Test Users list, or consent is refused.
- **Files inside the project** — keep `client_secret.json` and `token.json` in the **external** secret folder, not in `007/`.
- **Scope too narrow** — if you only added a Gmail *draft* scope, *send* and *read* calls will fail. Add read + send + calendar scopes for the assignment.
- **Submission address** — send to `rmisegal+uoh26b@gmail.com` verbatim; don't drop the `+uoh26b` tag.
- **Snake_case everywhere** — avoids space/encoding issues in project and file names.

---

## 9. Quick Checklist

**Video 1 — client**
- [ ] Cloud project created (snake_case team name)
- [ ] Gmail API enabled
- [ ] Calendar API enabled
- [ ] OAuth client ID created (External, Test User)
- [ ] Gmail + Calendar scopes added
- [ ] Desktop client created and JSON downloaded to **external secret folder**
- [ ] Client renamed (e.g. `my_google_safe.json`)
- [ ] Test users added (you + teammates)

**Video 2 — token + proof**
- [ ] Logged in as a registered test user
- [ ] Project folder created (`007/`), client/token kept external
- [ ] `uv` installed
- [ ] Python test program generated (with README)
- [ ] Env var points to client + token
- [ ] 1st run → consent in browser → `token.json` created
- [ ] 2nd run → draft appears in Gmail + event appears in Calendar

**Assignment (beyond the demo)**
- [ ] Read scope working (`read_emails`)
- [ ] Meeting extraction working (`extract_meeting`)
- [ ] Calendar event from extracted time (`add_calendar_event`)
- [ ] Real **send** working (`send_email`)
- [ ] Completion email sent to `rmisegal+uoh26b@gmail.com`
- [ ] Token-recovery path tested (delete → re-consent)