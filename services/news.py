"""
Hent dagsaktuelle nyhetsartikler om et selskap.

Strategi:
  1. NewsAPI (hvis NEWS_API_KEY er satt) – best kvalitet
  2. Google News RSS + BeautifulSoup – gratis fallback uten API-nøkkel
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from config import settings

# Selskapsendelser vi fjerner for bedre søkeresultater
_COMPANY_SUFFIXES = (" AS", " ASA", " BA", " DA", " NUF", " SA", " ANS", " ENK", " SE")


@dataclass
class NewsArticle:
    """Én nyhetsartikkel normalisert til felles format."""

    title: str
    source: str
    published: str
    summary: str
    url: str
    provider: str  # "newsapi" eller "google_news"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class NewsFetchError(Exception):
    """Feil ved henting av nyheter."""


def build_search_query(company_name: str) -> str:
    """
    Gjør Brreg-navn om til et bedre søkeord.

    "HYDRO ALUMINIUM AS" → "Hydro Aluminium"
    """
    name = company_name.strip()
    upper = name.upper()
    for suffix in _COMPANY_SUFFIXES:
        if upper.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name.strip().title() if name.isupper() else name.strip()


def _clean_text(text: str) -> str:
    """Fjern HTML og overflødig whitespace."""
    if not text:
        return ""
    cleaned = BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", cleaned)


def _format_date(raw: str) -> str:
    """Normaliser dato til lesbart format."""
    if not raw:
        return "Ukjent dato"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return raw[:10] if len(raw) >= 10 else raw


def _build_newsapi_query(query: str) -> str:
    """Presis NewsAPI-søkestreng med anførselstegn for bedre treff."""
    return f'"{query}"'


def _is_relevant(title: str, summary: str, query: str) -> bool:
    """Filtrer bort artikler som ikke faktisk handler om selskapet."""
    text = f"{title} {summary}".lower()
    query_lower = query.lower()

    if query_lower in text:
        return True

    words = [w for w in query_lower.split() if len(w) > 3]
    if words:
        return all(word in text for word in words)

    return any(word in text for word in query_lower.split() if len(word) > 2)


def _dedupe_articles(articles: list[NewsArticle]) -> list[NewsArticle]:
    """Fjern duplikater basert på tittel."""
    seen: set[str] = set()
    unique: list[NewsArticle] = []
    for article in articles:
        key = article.title.lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(article)
    return unique


def _fetch_from_newsapi(query: str, limit: int) -> list[NewsArticle]:
    """Hent artikler via NewsAPI (krever gratis API-nøkkel)."""
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": _build_newsapi_query(query),
            "sortBy": "publishedAt",
            "pageSize": max(limit * 5, 10),
            "searchIn": "title,description",
        },
        headers={"X-Api-Key": settings.news_api_key},
        timeout=15,
    )

    if not response.ok:
        raise NewsFetchError(f"NewsAPI returnerte HTTP {response.status_code}")

    articles: list[NewsArticle] = []
    for item in response.json().get("articles", []):
        title = _clean_text(item.get("title", ""))
        summary = _clean_text(item.get("description", "")) or "Ingen sammendrag tilgjengelig."

        if not title or title == "[Removed]":
            continue
        if not _is_relevant(title, summary, query):
            continue

        articles.append(
            NewsArticle(
                title=title,
                source=item.get("source", {}).get("name", "Ukjent kilde"),
                published=_format_date(item.get("publishedAt", "")),
                summary=summary,
                url=item.get("url", ""),
                provider="newsapi",
            )
        )

    return _dedupe_articles(articles)[:limit]


def _fetch_from_google_news(query: str, limit: int) -> list[NewsArticle]:
    """
    Gratis fallback: Google News RSS-feed.

    BeautifulSoup parser XML-strukturen og henter tittel, dato og kilde.
    """
    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}+when:30d&hl=no&gl=NO&ceid=NO:no"
    )

    response = requests.get(
        rss_url,
        headers={"User-Agent": "B2B-Scout/1.0"},
        timeout=15,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall(".//item")[:limit]

    articles: list[NewsArticle] = []
    for item in items:
        title = _clean_text(item.findtext("title", default=""))
        if not title:
            continue

        source = "Google News"
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            if len(parts) == 2:
                title, source = parts[0].strip(), parts[1].strip()

        pub_date = item.findtext("pubDate", default="")
        link = item.findtext("link", default="")
        description = _clean_text(item.findtext("description", default=""))

        articles.append(
            NewsArticle(
                title=title,
                source=source,
                published=pub_date[:16] if pub_date else "Nylig",
                summary=description or "Ingen sammendrag tilgjengelig.",
                url=link,
                provider="google_news",
            )
        )

    return articles


def fetch_company_news(company_name: str, limit: int = 3) -> list[NewsArticle]:
    """
    Hent de nyeste artiklene om et selskap.

    Prøver NewsAPI først hvis nøkkel finnes, ellers Google News RSS.
    """
    query = build_search_query(company_name)

    if settings.news_api_key:
        try:
            articles = _fetch_from_newsapi(query, limit)
            if len(articles) >= 1:
                return articles
        except (NewsFetchError, requests.RequestException):
            pass  # Fall through to Google News

    try:
        return _fetch_from_google_news(query, limit)
    except requests.RequestException as exc:
        raise NewsFetchError(f"Kunne ikke hente nyheter: {exc}") from exc


def articles_to_dicts(articles: list[NewsArticle]) -> list[dict[str, Any]]:
    """Konverter til JSON-serialiserbar liste."""
    return [a.to_dict() for a in articles]
