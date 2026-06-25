"""Gmail/Calendar agent tools: read emails, extract meetings, write events.

All tools are dependency-injected with already-built Google service objects
(or an injected LLM), so they are fully offline-testable with fakes.
"""
