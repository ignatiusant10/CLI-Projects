"""
Unit tests using pytest.

Enterprise habit: NEVER let tests touch your real data/journal.json.
We use pytest's `tmp_path` fixture + monkeypatch to redirect storage to a
temporary file for every test, so tests are isolated and repeatable.

Run with:  pytest tests/ -v
"""

import pytest
from pathlib import Path

from journal import storage, operations
from journal.exceptions import ValidationError, EntryNotFoundError


@pytest.fixture(autouse=True)
def use_temp_storage(tmp_path, monkeypatch):
    """Redirect DEFAULT_DATA_FILE to a temp path for every test automatically."""
    temp_file = tmp_path / "test_journal.json"
    monkeypatch.setattr(storage, "DEFAULT_DATA_FILE", temp_file)

    # operations.py imports load_entries/save_entries directly, so patch there too
    monkeypatch.setattr(
        operations, "load_entries",
        lambda: storage.load_entries(temp_file)
    )
    monkeypatch.setattr(
        operations, "save_entries",
        lambda entries: storage.save_entries(entries, temp_file)
    )
    yield temp_file


def test_add_entry_creates_entry_with_valid_data():
    entry = operations.add_entry("My first entry", "2026-09-03")
    assert entry.content == "My first entry"
    assert entry.entry_date == "2026-09-03"
    assert entry.id is not None


def test_add_entry_rejects_empty_content():
    with pytest.raises(ValidationError):
        operations.add_entry("   ", "2026-09-03")


def test_add_entry_rejects_invalid_date():
    with pytest.raises(ValidationError):
        operations.add_entry("Some content", "03-09-2026")  # wrong format


def test_view_entries_returns_all_added_entries():
    operations.add_entry("Entry one", "2026-09-01")
    operations.add_entry("Entry two", "2026-09-02")
    entries = operations.view_entries()
    assert len(entries) == 2


def test_view_entries_sorted_newest_first():
    operations.add_entry("Old entry", "2026-01-01")
    operations.add_entry("New entry", "2026-09-03")
    entries = operations.view_entries()
    assert entries[0].content == "New entry"


def test_search_entries_finds_keyword_case_insensitive():
    operations.add_entry("I love Python programming", "2026-09-01")
    operations.add_entry("Nothing relevant here", "2026-09-02")
    results = operations.search_entries("PYTHON")
    assert len(results) == 1
    assert "Python" in results[0].content


def test_search_entries_rejects_empty_keyword():
    with pytest.raises(ValidationError):
        operations.search_entries("")


def test_delete_entry_removes_correct_entry():
    entry = operations.add_entry("To be deleted", "2026-09-03")
    operations.delete_entry(entry.id)
    assert len(operations.view_entries()) == 0


def test_delete_nonexistent_entry_raises_error():
    with pytest.raises(EntryNotFoundError):
        operations.delete_entry("fake-id-that-does-not-exist")


def test_load_entries_handles_missing_file_gracefully(tmp_path):
    missing_file = tmp_path / "does_not_exist.json"
    entries = storage.load_entries(missing_file)
    assert entries == []


def test_load_entries_handles_corrupt_json(tmp_path):
    corrupt_file = tmp_path / "corrupt.json"
    corrupt_file.write_text("{ this is not valid json !!!")
    from journal.exceptions import CorruptDataError
    with pytest.raises(CorruptDataError):
        storage.load_entries(corrupt_file)