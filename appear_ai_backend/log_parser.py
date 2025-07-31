"""
log_parser.py
=================

This module provides simple utilities for parsing web server log files
and extracting information about visits from AI bots. Many AI search
engines deploy their own crawlers to discover content; identifying
their activity helps determine whether a site is being indexed for
generative responses.

The parser is designed for common access log formats (e.g., Apache
combined logs). It looks for known AI bot user agents and counts
visits per bot and per URL. The list of user agents can be extended
to include new crawlers as they emerge.

"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


# A mapping of friendly bot names to substrings found in their user agent
AI_BOT_SIGNATURES = {
    "ChatGPT-User": "ChatGPT-User",
    "GPTBot": "GPTBot",
    "OAI-SearchBot": "OAI-SearchBot",
    "ClaudeBot": "ClaudeBot",
    "Claude-Web": "Claude-Web",
    "CCBot": "CCBot",
    "PerplexityBot": "PerplexityBot",
    "Anthropic-AI": "Anthropic-ai",
    "Bytespider": "Bytespider",
    "Amazonbot": "Amazonbot",
    "Meta-ExternalAgent": "Meta-ExternalAgent",
    "YouBot": "YouBot",
}


LOG_LINE_RE = re.compile(
    r"^(?P<host>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] \"(?P<request>[^\"]+)\" (?P<status>\d{3}) (?P<size>\S+) \"(?P<referer>[^\"]*)\" \"(?P<user_agent>[^\"]*)\""
)


@dataclass
class CrawlEvent:
    """Representation of a single crawl event by an AI bot."""
    bot: str
    url: str
    timestamp: str


class LogParser:
    """Parse web server log files to extract AI bot visits."""

    def __init__(self, bot_signatures: Dict[str, str] | None = None) -> None:
        self.bot_signatures = bot_signatures or AI_BOT_SIGNATURES

    def parse_lines(self, lines: Iterable[str]) -> List[CrawlEvent]:
        """Parse lines from an access log and return a list of crawl events.

        Parameters
        ----------
        lines : Iterable[str]
            The lines of the log file.

        Returns
        -------
        List[CrawlEvent]
            A list of crawl events with bot name, URL and timestamp.
        """
        events: List[CrawlEvent] = []
        for line in lines:
            match = LOG_LINE_RE.match(line)
            if not match:
                continue
            user_agent = match.group("user_agent")
            request = match.group("request")
            timestamp = match.group("timestamp")
            # Request format: "GET /path HTTP/1.1"
            request_parts = request.split()
            url = request_parts[1] if len(request_parts) > 1 else ""
            for bot_name, signature in self.bot_signatures.items():
                if signature.lower() in user_agent.lower():
                    events.append(CrawlEvent(bot=bot_name, url=url, timestamp=timestamp))
                    break
        return events

    def summarize(self, events: Iterable[CrawlEvent]) -> Dict[str, Dict[str, int]]:
        """Summarize crawl events into counts per bot and per URL.

        Returns a nested dictionary of the form ``{bot: {url: count}}``.
        """
        summary: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))  # type: ignore
        for event in events:
            summary[event.bot][event.url] += 1
        return summary
