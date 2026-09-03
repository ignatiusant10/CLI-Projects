from dataclasses import dataclass, field, asdict
from datetime import datetime, date
import uuid

@dataclass
class Entry:
    content: str
    entry_date: str
    id: str = field(default_factory= lambda: str(uuid.uuid4()))
    created_at : str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Entry":
        return Entry(
            content=data['content'],
            entry_date=data['entry_date'],
            id=data['id'],
            created_at=data['created_at'],
        )
    @staticmethod
    def validate_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    @staticmethod
    def today() -> str:
        return date.today().isoformat()