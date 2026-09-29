import json
import re
from datetime import datetime
from urllib.parse import urljoin

import requests
import tldextract
from bs4 import BeautifulSoup


def clean_headline(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_date(text):
    patterns = [
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0)

    return datetime.now().strftime("%B %d, %Y")


def classify_signal(headline):
    text = headline.lower()

    if any(word in text for word in [
        "launch",
        "launches",
        "introduced",
        "introduces",
        "unveil",
        "unveils",
        "debut",
        "new product"
    ]):
        return "Product Launch"

    if any(word in text for word in [
        "price",
        "pricing",
        "cost",
        "subscription"
    ]):
        return "Pricing"

    if any(word in text for word in [
        "partner",
        "partners",
        "partnership",
        "collaboration",
        "collaborate",
        "joins forces"
    ]):
        return "Partnership"

    if any(word in text for word in [
        "funding",
        "investment",
        "invests",
        "raises",
        "raised",
        "million"
    ]):
        return "Funding"

    if any(word in text for word in [
        "acquire",
        "acquires",
        "acquisition"
    ]):
        return "Acquisition"

    if any(word in text for word in [
        "expand",
        "expands",
        "expansion",
        "opens",
        "enters",
        "entering"
    ]):
        return "Expansion"

    return "Update"


def get_headline(tag):
    text = clean_headline(
        tag.get_text(" ", strip=True)
    )

    if not text:
        return None

    if len(text) < 20 or len(text) > 300:
        return None

    return text


def detect_competitor(url):
    """
    Detect the main registered domain from any URL.

    Examples:

    https://newsroom.ibm.com/
    -> IBM

    https://blog.google.com/
    -> Google

    https://www.apple.com/
    -> Apple

    https://www.bbc.co.uk/
    -> BBC
    """

    extracted = tldextract.extract(url)

    if not extracted.domain:
        return "Unknown"

    competitor = extracted.domain

    return competitor.replace("-", " ").title()


def scrape_page(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/153.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unnecessary elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()

    signals = []
    seen = set()

    # Search headings and links
    for tag in soup.find_all([
        "h1",
        "h2",
        "h3",
        "a"
    ]):

        headline = get_headline(tag)

        if not headline:
            continue

        # Avoid duplicate headlines
        key = headline.lower()

        if key in seen:
            continue

        seen.add(key)

        # Get source URL
        source_url = tag.get("href")

        if source_url:
            source_url = urljoin(
                url,
                source_url
            )
        else:
            source_url = url

        signal_type = classify_signal(
            headline
        )

        date = extract_date(
            headline
        )

        signals.append({
            "type": signal_type,
            "headline": headline,
            "date": date,
            "source_url": source_url
        })

        # Keep maximum 20 signals
        if len(signals) >= 20:
            break

    return signals


def main():

    print("\n=== SignalHunter Web Scraper ===\n")

    url = input(
        "Enter competitor URL: "
    ).strip()

    if not url:
        print("URL is required.")
        return

    # Add HTTPS if user forgot the protocol
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        # Detect competitor automatically
        competitor = detect_competitor(url)

        print(
            f"\nDetected competitor: {competitor}"
        )

        # Scrape website
        signals = scrape_page(url)

        # Add competitor to every signal
        for signal in signals:
            signal["competitor"] = competitor

        # Create final JSON
        output = {
            "competitor": competitor,
            "source": url,
            "scraped_at": datetime.now().isoformat(),
            "signals_found": len(signals),
            "signals": signals
        }

        # Save JSON
        with open(
            "backend/signals.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=2,
                ensure_ascii=False
            )

        print("\nScraping completed!")
        print(
            f"Signals found: {len(signals)}"
        )
        print(
            "Saved to: backend/signals.json"
        )

    except requests.RequestException as e:

        print(
            f"\nRequest failed: {e}"
        )

    except Exception as e:

        print(
            f"\nError: {e}"
        )


if __name__ == "__main__":
    main()