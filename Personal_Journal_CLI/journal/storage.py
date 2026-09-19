# imporing required classes-------------------------------
import json
import os
import shutil
import logging
from pathlib import Path
from typing import List
# Importing Error handling classses------------------------
from journal.exceptions import StorageError,CorruptDataError

logger = logging.getLogger(__name__)

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "journal.json"

# Error handling for storage section------------------------------------------------

def ensure_file_exist(file_path: Path = DEFAULT_DATA_FILE) -> None:
     try:
          file_path.parent.mkdir(parents=True, exist_ok=True)
          if not file_path.exists():
               file_path.write_text("[]", encoding="utf-8")
               logger.info(f"Created new data file at {file_path}")
     except OSError as e:
          raise StorageError(f"could not create data file at {file_path}: {e}")

# Loading Entries Logic--------------------------------------------------------------

def load_entries(file_path: Path = DEFAULT_DATA_FILE) -> list[dict]:
     ensure_file_exist(file_path)

     try:
          raw_text = file_path.read_text(encoding="utf-8").strip()
     except OSError as e:
          raise StorageError(f"could not read data file : {e}")
     if not raw_text:
          return []

     try:
          data = json.loads(raw_text)
          if not isinstance(data, list):
               raise CorruptDataError("Data file doest not contain a JSON array. ")
          return data
     except json.JSONDecodeError as e:
          _backup_corrupt_file(file_path)
          raise CorruptDataError(
               f"Data file was corrupted and has been backed up. starting fresh. Details: {e}"
          )

def save_entries( entries: List[dict], file_path: Path = DEFAULT_DATA_FILE) -> None:
     ensure_file_exist(file_path)
     temp_path = file_path.with_suffix(".tmp")

     try:
          temp_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding ="utf-8")
          shutil.move(str(temp_path), str(file_path))
     except OSError as e:
          if temp_path.exists():
               temp_path.unlink(missing_ok=True)
          raise StorageError(f"Could not save data file: {e}")  



def _backup_corrupt_file(file_path: Path) -> None:
        backup_path = file_path.with_suffix(".corrupt.bak")
        try:
             shutil.copy(file_path, backup_path)
             file_path.write_text("[]", encoding="utf-8")
             logger.warning(f"corrupt file backed up to {backup_path}")
        except OSError as e:
             logger.error(f"failed to backup corrupt file: {e}")
