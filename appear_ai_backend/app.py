"""
app.py
========

This module defines a minimal FastAPI application exposing endpoints to
upload log files, run AI queries and generate exposure reports. It
serves as a starting point for the appear‑AI backend service. You
should run this app with a production ASGI server such as Uvicorn.

Example command to run locally::

    uvicorn appear_ai_backend.app:app --reload --port 8000

API overview:

* ``POST /upload-log`` – Accepts a log file and parses it for AI bot
  crawl events. Returns the summary statistics.
* ``POST /analyse`` – Runs AI queries for a given brand and optional
  keywords, generates a free report and returns it as plain text.

Future versions of this service can incorporate authentication,
payment, user accounts and persistent storage.
"""

from __future__ import annotations

import io
import os
from typing import List, Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import PlainTextResponse

from .ai_scraper import AIScraper
from .log_parser import LogParser
from .report_generator import generate_report

app = FastAPI(title="Appear‑AI Backend", description="API for AI exposure analysis.")


@app.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    """Parse a web server log file and return AI crawler statistics.

    The file should be in a standard access log format. The response
    contains the number of requests per AI bot and per URL.
    """
    content = await file.read()
    lines = content.decode(errors="ignore").splitlines()
    parser = LogParser()
    events = parser.parse_lines(lines)
    summary = parser.summarize(events)
    return {"events": len(events), "summary": summary}


@app.post("/analyse", response_class=PlainTextResponse)
async def analyse(
    brand: str = Form(...),
    keywords: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None),
):
    """Run AI queries and optional log analysis, then return a free report.

    Parameters
    ----------
    brand : str
        The brand or website name to query for.
    keywords : str, optional
        Comma‑separated list of keywords relevant to the brand.
    log_file : UploadFile, optional
        Optional log file for crawl analysis.

    Returns
    -------
    str
        A markdown report summarising findings.
    """
    kw_list: List[str] = []
    if keywords:
        kw_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    # Instantiate scraper
    scraper = AIScraper()
    queries = scraper.generate_queries(brand, kw_list)
    responses = scraper.run_queries(brand, queries)
    # Parse logs if provided
    parser = LogParser()
    events = []
    summary = {}
    if log_file:
        content = await log_file.read()
        lines = content.decode(errors="ignore").splitlines()
        events = parser.parse_lines(lines)
        summary = parser.summarize(events)
    # Generate report
    report = generate_report(brand, responses, events, summary)
    return report
