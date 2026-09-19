## Enterprise level exeption handling------------------------------------------------
class journalError(Exception):
    pass
class StorageError(journalError):
    pass
class CorruptDataError(StorageError):
    pass
class EntryNotFoundError(journalError):
    pass
class ValidationError(journalError):
    pass
