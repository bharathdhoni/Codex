#!/usr/bin/env python3
"""Gather recent NIFTY-related news and estimate a simple bull/bear signal.

Examples:
    python nifty_news.py
    python nifty_news.py --query "Nifty Bank" --limit 15
    python nifty_news.py --source bing --json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Iterable

RSS_SOURCES: dict[str, str] = {
    "google": "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en",
    "bing": "https://www.bing.com/news/search?q={query}&format=rss",
}

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

BULLISH_TERMS = {
    "rally",
    "gain",
    "gains",
    "surge",
    "up",
    "rise",
    "rises",
    "record high",
    "buy",
    "bull",
    "bullish",
    "optimism",
    "beat",
    "strong",
    "growth",
}

BEARISH_TERMS = {
    "fall",
    "falls",
    "drop",
    "drops",
    "slump",
    "down",
    "crash",
    "sell",
    "bear",
    "bearish",
    "weak",
    "concern",
    "fear",
    "miss",
    "loss",
}


def _fetch_rss(url: str) -> bytes:
    request = urllib.request.Request(url=url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def _parse_rss(rss_data: bytes, limit: int, source: str) -> list[dict[str, str]]:
    root = ET.fromstring(rss_data)
    items = root.findall("./channel/item")

    news = []
    for item in items[:limit]:
        news.append(
            {
                "source": source,
                "title": item.findtext("title", default="No title").strip(),
                "link": item.findtext("link", default="").strip(),
                "published": item.findtext("pubDate", default="").strip(),
            }
        )
    return news


def fetch_news(query: str, limit: int = 10, source: str = "auto") -> list[dict[str, str]]:
    encoded_query = urllib.parse.quote_plus(query)
    source_order: Iterable[str]

    if source == "auto":
        source_order = ("google", "bing")
    else:
        source_order = (source,)

    failures: list[str] = []
    for selected_source in source_order:
        url_template = RSS_SOURCES[selected_source]
        url = url_template.format(query=encoded_query)
        try:
            rss_data = _fetch_rss(url)
            parsed = _parse_rss(rss_data=rss_data, limit=limit, source=selected_source)
            if parsed:
                return parsed
            failures.append(f"{selected_source}: no items found")
        except Exception as exc:  # pragma: no cover - depends on runtime/network
            failures.append(f"{selected_source}: {exc}")

    raise RuntimeError("All RSS sources failed. " + " | ".join(failures))


def market_signal(news_items: list[dict[str, str]]) -> tuple[str, int, int]:
    """Return market signal as BULL, BEAR, or NULL using headline keyword counts."""
    bullish_score = 0
    bearish_score = 0

    for item in news_items:
        title = item.get("title", "").lower()
        title = re.sub(r"\s+", " ", title)

        bullish_score += sum(1 for term in BULLISH_TERMS if term in title)
        bearish_score += sum(1 for term in BEARISH_TERMS if term in title)

    if bullish_score > bearish_score:
        return "BULL", bullish_score, bearish_score
    if bearish_score > bullish_score:
        return "BEAR", bullish_score, bearish_score
    return "NULL", bullish_score, bearish_score


def format_news(news_items: list[dict[str, str]]) -> str:
    if not news_items:
        return "No news found.\nToday market view: NULL"

    signal, bull_score, bear_score = market_signal(news_items)

    lines = []
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append(f"Fetched at: {timestamp}")
    lines.append(f"Today market view: {signal} (bull={bull_score}, bear={bear_score})")
    lines.append("")

    for idx, item in enumerate(news_items, start=1):
        lines.append(f"{idx}. {item['title']}")
        lines.append(f"   Source: {item['source']}")
        if item["published"]:
            lines.append(f"   Published: {item['published']}")
        lines.append(f"   Link: {item['link']}")
        lines.append("")

    return "\n".join(lines).rstrip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gather latest NIFTY news headlines.")
    parser.add_argument(
        "--query",
        default="Nifty 50",
        help="Search query for the news provider (default: 'Nifty 50').",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of headlines to show (default: 10).",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "google", "bing"),
        default="auto",
        help="RSS source to use (default: auto fallback).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON output instead of formatted text.",
    )
    parser.add_argument(
        "--signal-only",
        action="store_true",
        help="Print only today's market view (BULL/BEAR/NULL).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.limit <= 0:
        print("Error: --limit must be a positive integer.", file=sys.stderr)
        return 1

    try:
        news_items = fetch_news(query=args.query, limit=args.limit, source=args.source)
    except Exception as exc:
        print(f"Failed to fetch news: {exc}", file=sys.stderr)
        return 1

    signal, bull_score, bear_score = market_signal(news_items)

    if args.signal_only:
        print(f"Today market view: {signal} (bull={bull_score}, bear={bear_score})")
    elif args.json:
        print(
            json.dumps(
                {
                    "market_view": signal,
                    "scores": {"bull": bull_score, "bear": bear_score},
                    "items": news_items,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_news(news_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
