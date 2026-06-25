"""Offline tests for the Gmail/Calendar agent tools (fake services injected)."""

from __future__ import annotations

import base64

from marl_cop_thief.services.google_agent.calendar_writer import add_calendar_event
from marl_cop_thief.services.google_agent.email_reader import read_emails
from marl_cop_thief.services.google_agent.meeting_extractor import extract_meeting
from marl_cop_thief.shared.gmail_client import send_email
from marl_cop_thief.shared.models import Meeting


class _FakeMessages:
    def __init__(self, listing, gets, sends):
        self._listing = listing
        self._gets = gets
        self._sends = sends
        self.sent_body = None

    def list(self, userId, q, maxResults):  # noqa: N803
        assert userId == "me"
        self._q, self._max = q, maxResults
        return _Exec(self._listing)

    def get(self, userId, id):  # noqa: A002, N803
        assert userId == "me"
        return _Exec(self._gets[id])

    def send(self, userId, body):  # noqa: N803
        assert userId == "me"
        self.sent_body = body
        return _Exec(self._sends)


class _Exec:
    def __init__(self, value):
        self._value = value

    def execute(self):
        return self._value


class _FakeGmail:
    def __init__(self, listing=None, gets=None, sends=None):
        self._messages = _FakeMessages(listing or {}, gets or {}, sends or {})

    def users(self):
        return self

    def messages(self):
        return self._messages


class _FakeEvents:
    def __init__(self, result):
        self._result = result
        self.body = None

    def insert(self, calendarId, body):  # noqa: N803
        assert calendarId == "primary"
        self.body = body
        return _Exec(self._result)


class _FakeCalendar:
    def __init__(self, result):
        self._events = _FakeEvents(result)

    def events(self):
        return self._events


class _FakeLLM:
    def __init__(self, response=None, raises=False):
        self._response = response
        self._raises = raises
        self.prompt = None

    def complete(self, prompt):
        self.prompt = prompt
        if self._raises:
            raise RuntimeError("llm down")
        return self._response


def test_read_emails_returns_id_and_snippet():
    listing = {"messages": [{"id": "a1"}, {"id": "b2"}]}
    gets = {
        "a1": {"id": "a1", "snippet": "hello"},
        "b2": {"id": "b2"},
    }
    gmail = _FakeGmail(listing=listing, gets=gets)
    out = read_emails(gmail, query="is:unread", max_results=5)
    assert out == [
        {"id": "a1", "snippet": "hello"},
        {"id": "b2", "snippet": ""},
    ]


def test_read_emails_empty_listing():
    gmail = _FakeGmail(listing={})
    assert read_emails(gmail) == []


def test_extract_meeting_success():
    llm = _FakeLLM("Standup | 2026-06-25T09:00 | 2026-06-25T09:30")
    meeting = extract_meeting(llm, "Let's meet tomorrow.")
    assert meeting == Meeting(
        title="Standup", start="2026-06-25T09:00", end="2026-06-25T09:30"
    )
    assert "EMAIL:" in llm.prompt


def test_extract_meeting_too_few_parts_returns_none():
    llm = _FakeLLM("NONE")
    assert extract_meeting(llm, "no meeting here") is None


def test_extract_meeting_empty_field_returns_none():
    llm = _FakeLLM("Title | | 2026-06-25T09:30")
    assert extract_meeting(llm, "garbage") is None


def test_extract_meeting_llm_raises_returns_none():
    llm = _FakeLLM(raises=True)
    assert extract_meeting(llm, "boom") is None


def test_add_calendar_event_returns_id_and_link():
    cal = _FakeCalendar({"id": "evt1", "htmlLink": "http://cal/evt1"})
    meeting = Meeting(
        title="Sync", start="2026-06-25T10:00", end="2026-06-25T11:00", location="Room 4"
    )
    out = add_calendar_event(cal, meeting)
    assert out == {"id": "evt1", "htmlLink": "http://cal/evt1"}
    body = cal.events().body
    assert body["summary"] == "Sync"
    assert body["description"] == "Room 4"
    assert body["start"] == {"dateTime": "2026-06-25T10:00"}
    assert body["end"] == {"dateTime": "2026-06-25T11:00"}


def test_add_calendar_event_no_location_uses_empty_description():
    cal = _FakeCalendar({"id": "e", "htmlLink": "l"})
    add_calendar_event(cal, Meeting(title="T", start="s", end="e"))
    assert cal.events().body["description"] == ""


def test_add_calendar_event_includes_timezone_when_given():
    # the Calendar API rejects offset-less datetimes without a timeZone (real-run fix)
    cal = _FakeCalendar({"id": "e", "htmlLink": "l"})
    add_calendar_event(cal, Meeting(title="T", start="2026-07-01T14:00:00",
                                    end="2026-07-01T15:00:00"), timezone="Asia/Jerusalem")
    body = cal.events().body
    assert body["start"] == {"dateTime": "2026-07-01T14:00:00", "timeZone": "Asia/Jerusalem"}
    assert body["end"] == {"dateTime": "2026-07-01T15:00:00", "timeZone": "Asia/Jerusalem"}


def test_send_email_returns_message_id():
    gmail = _FakeGmail(sends={"id": "msg-99"})
    msg_id = send_email(gmail, "to@example.com", "Hi", "Body text")
    assert msg_id == "msg-99"
    raw = gmail.messages().sent_body["raw"]
    decoded = base64.urlsafe_b64decode(raw.encode()).decode()
    assert "to@example.com" in decoded
    assert "Hi" in decoded
    assert "Body text" in decoded
