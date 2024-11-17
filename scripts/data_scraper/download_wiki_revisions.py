import argparse
from datetime import datetime
from pathlib import Path
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

DATA_DIR = Path("data")


def download_page_w_revisions(page_title: str) -> str:
    """Downloads complete revision history of a page using Special:Export with progress bar."""
    url = f"https://en.wikipedia.org/wiki/Special:Export/{page_title}"
    params = {"history": "", "action": "submit"}  # Empty parameter to get full history

    # Create a session with retry logic
    session = requests.Session()
    retries = Retry(
        total=5,  # Retry up to 5 times
        backoff_factor=1,  # Wait 1s, 2s, 4s, 8s, etc. between retries
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        # Make initial request to get content length
        response = session.get(url, params=params, stream=True)
        response.raise_for_status()

        # Get total size if available
        total_size = int(response.headers.get("content-length", 0))

        # Initialize progress bar
        progress = tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc="Downloading revisions",
            leave=True,
        )

        # Download with progress
        content = []
        for data in response.iter_content(chunk_size=8192):
            content.append(data)
            progress.update(len(data))

        return b"".join(content).decode("utf-8")
    except Exception as e:
        print(f"Error occurred while downloading: {e}")
        return ""
    finally:
        progress.close()


def parse_mediawiki_revisions(xml_content):
    soup = BeautifulSoup(xml_content, "lxml-xml")
    for revision in soup.find_all("revision"):
        yield str(revision)


def count_revisions_in_xml(xml_content: str) -> int:
    """Count the number of revisions in a single XML response."""
    soup = BeautifulSoup(xml_content, "lxml-xml")
    return len(soup.find_all("revision"))


def count_stored_revisions(page_name: str, data_dir: Path) -> dict:
    """
    Counts all stored revisions for a given page, organized by year and month.

    Returns:
        dict: A dictionary with total count and breakdowns by year and month
        Format: {
            'total': int,
            'by_year': {year: count, ...},
            'by_year_month_day': {(year, month, day): count, ...}
        }
    """
    page_dir = data_dir / page_name
    if not page_dir.exists():
        return {"total": 0, "by_year": {}, "by_year_month_day": {}}

    counts = {"total": 0, "by_year": {}, "by_year_month_day": {}}

    # Walk through the directory structure
    for year_dir in sorted(page_dir.iterdir()):
        if not year_dir.is_dir():
            continue

        year = year_dir.name
        counts["by_year"][year] = 0

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue

            month = month_dir.name
            revision_count = len(list(month_dir.glob("*.xml")))
            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue

                day = day_dir.name
                revision_count = len(list(day_dir.glob("*.xml")))

                counts["by_year"][year] += revision_count
                counts["by_year_month_day"][(year, month, day)] = revision_count
                counts["total"] += revision_count

    return counts


def format_revision_counts(page_name: str, counts: dict) -> str:
    """Formats the revision counts into a readable string."""
    if counts["total"] == 0:
        return f"No revisions found for '{page_name}'."

    # Basic summary
    output = [f"Found {counts['total']} total revisions for '{page_name}'."]

    # Year breakdown
    year_counts = counts["by_year"]
    if year_counts:
        output.append("\nBreakdown by year:")
        for year in sorted(year_counts.keys()):
            output.append(f"  {year}: {year_counts[year]} revisions")

    # Day breakdown (optional, commented out to avoid too much detail)
    day_counts = counts["by_year_month_day"]
    if day_counts:
        output.append("\nBreakdown by day:")
        for year, month, day in sorted(day_counts.keys()):
            output.append(
                f"  {year}-{month}-{day}: {day_counts[(year, month, day)]} revisions"
            )

    return "\n".join(output)


def main(page: str, data_dir: Path, count_only: bool = False):
    """
    Downloads all revisions of the given page title and organizes them by date.
    If count_only is True, just prints the count of stored revisions.
    """
    if count_only:
        counts = count_stored_revisions(page, data_dir)
        print(format_revision_counts(page, counts))
        return

    print(f"Downloading complete history of {page}")
    raw_revisions = download_page_w_revisions(page)

    # Count total revisions for progress bar
    total_revisions = len(BeautifulSoup(raw_revisions, "lxml-xml").find_all("revision"))
    print(f"Found {total_revisions} revisions. Organizing into directory structure...")

    for wiki_revision in tqdm(
        parse_mediawiki_revisions(raw_revisions), total=total_revisions
    ):
        revision_path = construct_path(
            wiki_revision=wiki_revision, page_name=page, save_dir=data_dir
        )
        if not revision_path.exists():
            revision_path.parent.mkdir(parents=True, exist_ok=True)
            revision_path.write_text(wiki_revision, encoding="utf-8")

    # Show final counts
    counts = count_stored_revisions(page, data_dir)
    print("\nFinal revision counts:")
    print(format_revision_counts(page, counts))


def extract_id(revision: str) -> str:
    return str(_extract_attribute(revision, attribute="id"))


def find_timestamp(revision: str) -> datetime:
    return parse_timestring(_extract_attribute(revision, attribute="timestamp"))


def _extract_attribute(text: str, attribute: str = "timestamp") -> str:
    soup = BeautifulSoup(text, "lxml-xml")
    result = soup.find(attribute)
    if result is None:
        raise ValueError(f"Could not find attribute {attribute} in text")
    return result.text


def parse_timestring(timestring: str) -> datetime:
    return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")


def extract_yearmonth(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m")


def extract_yearmonthday(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m-%d")


def find_yearmonth(revision: str) -> str:
    return extract_yearmonth(find_timestamp(revision))


def find_yearmonthday(revision: str) -> str:
    return extract_yearmonthday(find_timestamp(revision))


def construct_path(page_name: str, save_dir: Path, wiki_revision: str) -> Path:
    revision_id = extract_id(wiki_revision)
    timestamp = find_timestamp(wiki_revision)
    year = str(timestamp.year)
    month = str(timestamp.month).zfill(2)
    day = str(timestamp.day).zfill(2)
    revision_path = save_dir / page_name / year / month / day / f"{revision_id}.xml"
    return revision_path


def validate_page(page_name: str, page_xml: str) -> None:
    try:
        _ = _extract_attribute(page_xml, attribute="page")
    except ValueError:
        raise ValueError(f"Page {page_name} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Wikipedia page revisions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("page", type=str, help="Title of the Wikipedia page")
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Only count and display stored revisions without downloading",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help="Directory to store the revision data",
    )
    args = parser.parse_args()
    main(page=args.page, data_dir=args.data_dir, count_only=args.count_only)
