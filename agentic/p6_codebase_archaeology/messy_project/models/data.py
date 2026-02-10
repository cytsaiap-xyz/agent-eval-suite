"""Data model module."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class DataModel:
    """Generic data model."""

    id: str
    type: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update(self, content: Dict[str, Any]):
        """Update content."""
        self.content.update(content)
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# Dead code - never used collections
class DataCollection:
    """Collection of data models. Never instantiated."""

    def __init__(self):
        self._items: List[DataModel] = []

    def add(self, item: DataModel):
        self._items.append(item)

    def find(self, id: str) -> Optional[DataModel]:
        for item in self._items:
            if item.id == id:
                return item
        return None

    def filter(self, type: str) -> List[DataModel]:
        return [item for item in self._items if item.type == type]


# More dead code
def serialize_data(model: DataModel) -> str:
    """Serialize data model. Never called."""
    import json
    return json.dumps(model.to_dict())


def deserialize_data(json_str: str) -> DataModel:
    """Deserialize data model. Never called."""
    import json
    data = json.loads(json_str)
    return DataModel(
        id=data["id"],
        type=data["type"],
        content=data["content"],
        metadata=data.get("metadata", {}),
        created_at=datetime.fromisoformat(data["created_at"])
    )
