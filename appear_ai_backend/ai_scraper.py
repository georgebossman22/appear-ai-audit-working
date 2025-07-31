"""
ai_scraper.py
=================

This module defines the ``AIScraper`` class, which coordinates queries to
various generative AI platforms to determine whether a given brand or
website is mentioned. Each platform requires an API key, which must
be supplied via environment variables or configuration when the
scraper is instantiated.

The methods in this module are deliberately simple so that they can be
extended later. For example, the ``query_chatgpt`` method only
generates a placeholder response if no OpenAI API key is provided.

Usage example::

    from appear_ai_backend.ai_scraper import AIScraper

    scraper = AIScraper(openai_key="sk-...", claude_key="...", gemini_key="...")
    queries = scraper.generate_queries(brand="ExampleCorp", keywords=["AI", "analytics"])
    responses = scraper.run_queries(brand="ExampleCorp", queries=queries)
    # ``responses`` is a list of dictionaries with platform, prompt and response text.

"""

from __future__ import annotations

import logging
import os
from typing import Dict, Iterable, List, Optional

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # The openai library is optional; if not installed, calls will be skipped.

logger = logging.getLogger(__name__)


class AIScraper:
    """Query generative AI platforms for brand mentions.

    Parameters
    ----------
    openai_key : str, optional
        API key for OpenAI. If provided, will be used to query ChatGPT.
    claude_key : str, optional
        API key for Anthropic Claude. Placeholder for future use.
    gemini_key : str, optional
        API key for Google Gemini. Placeholder for future use.
    perplexity_key : str, optional
        API key for Perplexity. Placeholder for future use.

    """

    def __init__(
        self,
        openai_key: Optional[str] = None,
        claude_key: Optional[str] = None,
        gemini_key: Optional[str] = None,
        perplexity_key: Optional[str] = None,
    ) -> None:
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.claude_key = claude_key or os.getenv("CLAUDE_API_KEY")
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.perplexity_key = perplexity_key or os.getenv("PERPLEXITY_API_KEY")

        # Configure OpenAI if available and key provided
        if openai and self.openai_key:
            openai.api_key = self.openai_key

    def generate_queries(self, brand: str, keywords: Iterable[str]) -> List[str]:
        """Generate a list of query prompts for the AI platforms.

        The prompts are designed to elicit information about the brand and
        its products or services. They include general questions and
        keyword‑specific variations.

        Parameters
        ----------
        brand : str
            The brand or company name.
        keywords : Iterable[str]
            Keywords relevant to the brand's offerings.

        Returns
        -------
        List[str]
            A list of query prompts.
        """
        prompts: List[str] = []
        base_questions = [
            f"What do you know about {brand}?",
            f"How would you describe {brand}'s products or services?",
            f"What are some alternatives to {brand}?",
        ]
        prompts.extend(base_questions)
        for kw in keywords:
            prompts.append(f"Does {brand} have expertise in {kw}?")
            prompts.append(f"Best {kw} providers – does {brand} rank among them?")
        return prompts

    def query_chatgpt(self, prompt: str) -> str:
        """Query OpenAI's ChatGPT API for a given prompt.

        If the ``openai`` library is not installed or no API key is
        configured, a placeholder response is returned instead. The
        placeholder indicates that no real call was made.

        Parameters
        ----------
        prompt : str
            The prompt to send to ChatGPT.

        Returns
        -------
        str
            The text of the response.
        """
        if not openai or not self.openai_key:
            logger.debug("OpenAI not configured. Returning placeholder response.")
            return "[Placeholder] OpenAI API key not configured."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            # Extract the assistant's reply
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.exception("Error querying ChatGPT: %s", e)
            return f"[Error] {str(e)}"

    def query_claude(self, prompt: str) -> str:
        """Placeholder for querying Anthropic's Claude API.

        At present, this method returns a placeholder response because the
        Anthropic client library is not available by default in this
        environment. In production, you would import the client and send
        the prompt using the provided API key.
        """
        if not self.claude_key:
            return "[Placeholder] Claude API key not configured."
        return "[Placeholder] Claude integration not implemented."

    def query_gemini(self, prompt: str) -> str:
        """Placeholder for querying Google's Gemini API.

        A real implementation would call the Gemini generative AI API
        using the gemini_key. Currently returns a placeholder.
        """
        if not self.gemini_key:
            return "[Placeholder] Gemini API key not configured."
        return "[Placeholder] Gemini integration not implemented."

    def query_perplexity(self, prompt: str) -> str:
        """Placeholder for querying Perplexity's API.

        Perplexity does not have an official API at the time of writing,
        therefore this function returns a placeholder until an API
        becomes available or a browser automation solution is added.
        """
        if not self.perplexity_key:
            return "[Placeholder] Perplexity API key not configured."
        return "[Placeholder] Perplexity integration not implemented."

    def run_queries(self, brand: str, queries: List[str]) -> List[Dict[str, str]]:
        """Run a list of queries across all configured AI platforms.

        Parameters
        ----------
        brand : str
            The brand being analysed. Not currently used, but reserved
            for future context‑based prompting.
        queries : List[str]
            The list of prompts to send.

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries, each containing ``platform``, ``prompt`` and
            ``response`` keys.
        """
        results: List[Dict[str, str]] = []
        for prompt in queries:
            # ChatGPT
            chatgpt_response = self.query_chatgpt(prompt)
            results.append(
                {
                    "platform": "ChatGPT",
                    "prompt": prompt,
                    "response": chatgpt_response,
                }
            )
            # Claude
            claude_response = self.query_claude(prompt)
            results.append(
                {
                    "platform": "Claude",
                    "prompt": prompt,
                    "response": claude_response,
                }
            )
            # Gemini
            gemini_response = self.query_gemini(prompt)
            results.append(
                {
                    "platform": "Gemini",
                    "prompt": prompt,
                    "response": gemini_response,
                }
            )
            # Perplexity
            perplexity_response = self.query_perplexity(prompt)
            results.append(
                {
                    "platform": "Perplexity",
                    "prompt": prompt,
                    "response": perplexity_response,
                }
            )
        return results
