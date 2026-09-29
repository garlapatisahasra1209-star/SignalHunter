import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
import tldextract
from bs4 import BeautifulSoup


MAX_SIGNALS = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    )
}


def clean_text(text):
    """Clean extra spaces and unwanted characters."""
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_headline(text):
    """Clean and validate a possible headline."""
    text = clean_text(text)

    if len(text) < 15:
        return ""

    if len(text) > 250:
        return ""

    return text


def detect_competitor(url):
    """Detect competitor name from any domain/subdomain."""
    extracted = tldextract.extract(url)

    if not extracted.domain:
        return "Unknown"

    competitor = extracted.domain

    return competitor.replace("-", " ").title()


def classify_signal(headline):
    """Classify a headline into a competitive signal category."""

    text = headline.lower()

    if any(word in text for word in [
        "launch",
        "launches",
        "launched",
        "introduces",
        "introduced",
        "unveil",
        "unveils",
        "release",
        "released",
    ]):
        return "Product Launch"

    if any(word in text for word in [
        "price",
        "pricing",
        "priced",
        "cost",
        "subscription",
        "fee",
        "discount",
    ]):
        return "Pricing"

    if any(word in text for word in [
        "partner",
        "partnership",
        "partners",
        "collaboration",
        "collaborates",
        "alliance",
    ]):
        return "Partnership"

    if any(word in text for word in [
        "funding",
        "funded",
        "investment",
        "invests",
        "investor",
        "raised",
        "raises",
    ]):
        return "Funding"

    if any(word in text for word in [
        "acquire",
        "acquires",
        "acquisition",
        "merger",
        "merges",
    ]):
        return "Acquisition"

    if any(word in text for word in [
        "expand",
        "expansion",
        "expands",
        "opens",
        "opening",
        "enters",
        "entering",
        "market",
        "global",
    ]):
        return "Expansion"

    if any(word in text for word in [
        "update",
        "updated",
        "upgrade",
        "upgraded",
        "announces",
        "announcement",
    ]):
        return "Update"

    return "Strategic Move"


def extract_date(element):
    """Try to extract a publication date from an element."""

    time_tag = element.find("time")

    if time_tag:
        datetime_value = time_tag.get("datetime")

        if datetime_value:
            return clean_text(datetime_value)

        time_text = clean_text(time_tag.get_text(" ", strip=True))

        if time_text:
            return time_text

    return ""


def is_probable_article_link(link):
    """Check whether a link looks like an actual article/news link."""

    href = link.get("href")

    if not href:
        return False

    text = clean_headline(link.get_text(" ", strip=True))

    if not text:
        return False

    href_lower = href.lower()

    # Ignore obvious navigation/system links.
    ignored_words = [
        "/login",
        "/signin",
        "/signup",
        "/register",
        "/search",
        "/contact",
        "/privacy",
        "/terms",
        "/cookie",
        "/careers",
        "/jobs",
        "/about",
        "#",
        "javascript:",
        "mailto:",
    ]

    if any(word in href_lower for word in ignored_words):
        return False

    # Navigation words that are usually not article titles.
    navigation_words = [
        "home",
        "menu",
        "products",
        "services",
        "solutions",
        "company",
        "about us",
        "contact us",
        "careers",
        "resources",
        "support",
        "sign in",
        "log in",
    ]

    text_lower = text.lower()

    if text_lower in navigation_words:
        return False

    # Very short text is usually navigation.
    if len(text.split()) < 4:
        return False

    return True


def get_article_candidates(soup, base_url):
    """
    Find likely article/news items.

    Priority:
    1. <article> elements
    2. Containers with article/news/card/post classes
    3. Links as fallback
    """

    candidates = []

    # ---------------------------------------------------------
    # 1. ARTICLE ELEMENTS
    # ---------------------------------------------------------

    articles = soup.find_all("article")

    for article in articles:
        headline = ""

        for selector in [
            "h1",
            "h2",
            "h3",
            "[class*='title']",
            "[class*='headline']",
        ]:
            element = article.select_one(selector)

            if element:
                headline = clean_headline(
                    element.get_text(" ", strip=True)
                )

                if headline:
                    break

        if not headline:
            continue

        link_element = article.find("a", href=True)

        if not link_element:
            continue

        href = link_element.get("href")

        full_url = urljoin(base_url, href)

        date = extract_date(article)

        candidates.append({
            "headline": headline,
            "source_url": full_url,
            "date": date,
            "priority": 100,
        })

    # ---------------------------------------------------------
    # 2. NEWS / ARTICLE CONTAINERS
    # ---------------------------------------------------------

    containers = soup.select(
        "[class*='article'], "
        "[class*='news'], "
        "[class*='story'], "
        "[class*='post'], "
        "[class*='card']"
    )

    for container in containers:

        headline_element = None

        for selector in [
            "h1",
            "h2",
            "h3",
            "[class*='title']",
            "[class*='headline']",
        ]:
            headline_element = container.select_one(selector)

            if headline_element:
                break

        if not headline_element:
            continue

        headline = clean_headline(
            headline_element.get_text(" ", strip=True)
        )

        if not headline:
            continue

        link_element = container.find("a", href=True)

        if not link_element:
            continue

        href = link_element.get("href")

        full_url = urljoin(base_url, href)

        date = extract_date(container)

        candidates.append({
            "headline": headline,
            "source_url": full_url,
            "date": date,
            "priority": 80,
        })

    # ---------------------------------------------------------
    # 3. FALLBACK TO HEADLINE LINKS
    # ---------------------------------------------------------

    for link in soup.find_all("a", href=True):

        if not is_probable_article_link(link):
            continue

        headline = clean_headline(
            link.get_text(" ", strip=True)
        )

        if not headline:
            continue

        href = link.get("href")

        full_url = urljoin(base_url, href)

        parent = link.parent

        date = ""

        if parent:
            date = extract_date(parent)

        candidates.append({
            "headline": headline,
            "source_url": full_url,
            "date": date,
            "priority": 40,
        })

    return candidates


def scrape_page(url):
    """Scrape competitive signals from a webpage."""

    print("\nFetching:", url)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print("Could not fetch page:", e)
        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove elements that usually contain noise.
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        "header",
        "form",
    ]):
        tag.decompose()

    candidates = get_article_candidates(
        soup,
        url
    )

    # ---------------------------------------------------------
    # Remove duplicates
    # ---------------------------------------------------------

    unique = {}

    for item in candidates:

        headline_key = item["headline"].lower()

        if headline_key not in unique:
            unique[headline_key] = item
        else:
            # Keep the higher-quality candidate.
            if item["priority"] > unique[headline_key]["priority"]:
                unique[headline_key] = item

    candidates = list(unique.values())

    # ---------------------------------------------------------
    # Score candidates
    # ---------------------------------------------------------

    for item in candidates:

        score = item["priority"]

        headline = item["headline"].lower()
        url_lower = item["source_url"].lower()

        # Article/news URL indicators.
        if any(word in url_lower for word in [
            "/news/",
            "/article/",
            "/articles/",
            "/story/",
            "/stories/",
            "/press/",
            "/press-release/",
            "/press-releases/",
            "/blog/",
            "/2026/",
            "/2025/",
        ]):
            score += 20

        # Competitive signal keywords.
        if any(word in headline for word in [
            "launch",
            "launches",
            "introduced",
            "announces",
            "announced",
            "pricing",
            "price",
            "partnership",
            "funding",
            "acquisition",
            "expansion",
            "market",
            "investment",
            "product",
            "release",
        ]):
            score += 15

        # Having a publication date is a good signal.
        if item["date"]:
            score += 10

        item["score"] = score

    # Highest quality first.
    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # ---------------------------------------------------------
    # Convert to final signals
    # ---------------------------------------------------------

    signals = []

    for item in candidates[:MAX_SIGNALS]:

        signal = {
            "type": classify_signal(
                item["headline"]
            ),
            "headline": item["headline"],
            "date": item["date"],
            "source_url": item["source_url"],
        }

        signals.append(signal)

    return signals


def main():

    print("=" * 60)
    print("SIGNALHUNTER COMPETITIVE INTELLIGENCE SCRAPER")
    print("=" * 60)

    url = input(
        "\nEnter competitor/news URL: "
    ).strip()

    if not url:
        print("No URL provided.")
        return

    # Add https:// if the user didn't type it.
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    competitor = detect_competitor(url)

    print("\nCompetitor detected:", competitor)

    signals = scrape_page(url)

    if not signals:
        print(
            "\nNo useful signals were found."
        )
        return

    # Add competitor to every signal.
    for signal in signals:
        signal["competitor"] = competitor

    output = {
        "competitor": competitor,
        "source": url,
        "scraped_at": datetime.now().isoformat(),
        "signals_found": len(signals),
        "signals": signals,
    }

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

    print(
        f"\nSuccessfully collected {len(signals)} signals."
    )

    print(
        "\nSaved to:"
    )

    print(
        "backend/signals.json"
    )

    print("\nTop signals:")

    for index, signal in enumerate(
        signals[:10],
        start=1
    ):

        print(
            f"\n{index}. "
            f"[{signal['type']}] "
            f"{signal['headline']}"
        )


if __name__ == "__main__":
    main()