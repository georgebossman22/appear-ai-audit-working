"""
report_generator.py
====================

This module defines a simple report generator that compiles the results
from AI queries and log analysis into a human‑readable report. The
generator produces Markdown output that can be converted to PDF or
rendered in a web interface. It includes basic scoring logic and
recommendations derived from research into generative search
optimisation.

The recommendations here are illustrative. In a production system,
recommendations should be tailored to the specific gaps detected in
the data and supported with citations or references to current
best‑practice resources.
"""

from __future__ import annotations

import datetime
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from .log_parser import LogParser, CrawlEvent


def analyse_mentions(responses: Iterable[Dict[str, str]], brand: str) -> Tuple[int, int]:
    """Count how many responses mention the brand and how many do not.

    A simple keyword search is performed on the response text. This
    function returns the number of positive hits and the total number
    of responses.

    Parameters
    ----------
    responses : Iterable[Dict[str, str]]
        The list of response records from the AI scraper.
    brand : str
        The brand name to search for.

    Returns
    -------
    Tuple[int, int]
        A tuple (hits, total) where ``hits`` is the number of
        responses containing the brand (case‑insensitive) and ``total`` is
        the total number of responses analysed.
    """
    hits = 0
    total = 0
    for rec in responses:
        total += 1
        if brand.lower() in rec.get("response", "").lower():
            hits += 1
    return hits, total


def generate_report(
    brand: str,
    responses: List[Dict[str, str]],
    crawl_events: List[CrawlEvent],
    summary: Dict[str, Dict[str, int]]
) -> str:
    """Generate a Markdown report summarising AI exposure and crawl activity.

    Parameters
    ----------
    brand : str
        The brand or website being analysed.
    responses : List[Dict[str, str]]
        Results from AI queries.
    crawl_events : List[CrawlEvent]
        Parsed crawl events from log files.
    summary : Dict[str, Dict[str, int]]
        A nested dictionary summarising crawl counts per bot and URL.

    Returns
    -------
    str
        A Markdown string containing the report.
    """
    date_str = datetime.date.today().isoformat()
    hits, total = analyse_mentions(responses, brand)
    hit_rate = (hits / total * 100) if total else 0.0

    lines: List[str] = []
    lines.append(f"# AI Exposure Report for **{brand}**")
    lines.append("")
    lines.append(f"Generated on {date_str}")
    lines.append("")

    # Exposure summary
    lines.append("## Exposure Summary")
    lines.append("")
    lines.append(
        f"Out of **{total}** AI responses analysed across all platforms, **{hits}** mentioned the brand, "
        f"giving an approximate exposure rate of **{hit_rate:.1f}%**."
    )
    lines.append("")

    # Per‑platform breakdown
    platform_counts = defaultdict(lambda: {"hits": 0, "total": 0})  # type: ignore
    for rec in responses:
        platform = rec["platform"]
        platform_counts[platform]["total"] += 1
        if brand.lower() in rec["response"].lower():
            platform_counts[platform]["hits"] += 1
    lines.append("### Platform Breakdown")
    lines.append("")
    lines.append("| Platform | Mentions | Responses | Exposure Rate |")
    lines.append("|---|---:|---:|---:|")
    for platform, stats in platform_counts.items():
        hits_p = stats["hits"]
        total_p = stats["total"]
        rate_p = (hits_p / total_p * 100) if total_p else 0
        lines.append(f"| {platform} | {hits_p} | {total_p} | {rate_p:.1f}% |")
    lines.append("")

    # Crawl summary
    lines.append("## AI Bot Crawl Activity")
    lines.append("")
    if not crawl_events:
        lines.append("No crawl events were detected in the supplied log file. This may indicate that your site is not being visited by AI crawlers or the log file does not contain bot traffic.")
    else:
        lines.append(
            "The table below shows how many times each AI crawler accessed your site in the provided logs. Use this information to assess whether your content is being discovered."
        )
        lines.append("")
        lines.append("| Crawler | Pages Crawled | Total Requests |")
        lines.append("|---|---:|---:|")
        for bot, pages in summary.items():
            total_requests = sum(pages.values())
            lines.append(f"| {bot} | {len(pages)} | {total_requests} |")
        lines.append("")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    lines.append("Based on the data and current best practices in generative engine optimisation, consider the following actions:")
    lines.append("")
    lines.append("1. **Strengthen crawlability.** Ensure important pages are indexable and easily discoverable through internal linking. Check `robots.txt` and meta tags to avoid inadvertently blocking AI crawlers.")
    lines.append("2. **Develop comprehensive, factual content.** Create in‑depth guides and FAQs that answer common questions in your niche. Break content into clear sections with headings and bullet lists to aid passage‑level retrieval【761103843205367†L540-L545】.")
    lines.append("3. **Optimise for multiple query variations.** Use keyword research to identify different ways people might ask about your products and weave those variations naturally into your content【899395914591967†L246-L266】.")
    lines.append("4. **Earn citations on authoritative sites.** Digital PR and guest posts can generate brand mentions on trusted domains. AI platforms favour established sources【899395914591967†L269-L282】.")
    lines.append("5. **Monitor AI visibility regularly.** Repeat this analysis periodically to track improvements and respond to algorithm updates. Adjust your strategy based on changes in AI platform behaviour【899395914591967†L339-L345】.")
    lines.append("")

    lines.append("---")
    lines.append("This report was generated automatically. For more detailed guidance, consider upgrading to the full package.")

    return "\n".join(lines)
