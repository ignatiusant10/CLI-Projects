import logging
from typing import List, Optional

from journal.entry import Entry
from journal.storage import load_entries, save_entries
from journal.exceptions import EntryNotFoundError, ValidationError

logger = logging.getLogger(__name__)

# Adding entry logic---------------------------------------------------------------------

def add_entry(content: str, entry_date:Optional[str]=None )-> Entry:
    content=content.strip()
    if not content:
        raise ValidationError("Entry content cannot be empty.")

    entry_date = entry_date or Entry.today()
    if not Entry.validate_date(entry_date):
        raise ValidationError(f"Invalid date '{entry_date}'. Expected format: YYYY-MM-DD.")

    entry = Entry(content=content, entry_date= entry_date)
    entries = load_entries()
    entries.append(entry.to_dict())
    save_entries(entries)

    logger.info(f"Added entry {entry.id} dated {entry.entry_date}")
    return entry


# Viewing Entry logic-----------------------------------------------------------------------

def view_entries(sort_by_date: bool=True) -> list[Entry]:
    raw_entries = load_entries()
    entries = [Entry.from_dict(e) for e in raw_entries]

    if sort_by_date:
        entries.sort(key=lambda e: e.entry_date , reverse=True)
    return entries
def search_entries(keyword: str) ->list[Entry]:
    if not keyword or not keyword.strip():
        raise ValidationError("Search keyword cannot be empty. ")

    keyword = keyword.lower().strip()
    all_entries = view_entries()
    matches = [e for e in all_entries if keyword in e.content.lower()]

    logger.info(f"Search for '{keyword}' returned {len(matches)} result(s)")
    return matches

# Deleting Entry Logic--------------------------------------------------------------------------

def delete_entry(entry_id: str) -> None:
    entries = load_entries()
    filtered = [e for e in entries if e["id"] != entry_id]

    if len(filtered) == len(entries):
        raise EntryNotFoundError(f"No entry found with ID '{entry_id}'.")

    save_entries(filtered)
    logger.info(f"Deleted entry {entry_id}")

# get entry id logic-----------------------------------------------------------------------------

def get_entry_by_id(entry_id:str) -> Entry:
    entries = load_entries()
    for e in entries:
        if e["id"] == entry_id:
            return Entry.from_dict(e)
        raise EntryNotFoundError(f"No entry found with ID '{entry_id}'.")
