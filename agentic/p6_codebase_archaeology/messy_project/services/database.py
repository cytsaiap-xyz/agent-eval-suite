"""Database service."""

from typing import Any, Dict, List, Optional


class DatabaseConnection:
    """Database connection manager."""

    def __init__(self, config: Dict[str, Any]):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 5432)
        self.database = config.get("name", "myapp")
        self._connected = False
        self._data = {}  # In-memory storage for offline testing

    def connect(self):
        """Establish database connection."""
        self._connected = True

    def disconnect(self):
        """Close database connection."""
        self._connected = False

    def execute(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query."""
        if not self._connected:
            self.connect()
        # Simulated execution
        return []

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a record."""
        if table not in self._data:
            self._data[table] = []
        self._data[table].append(data)
        return len(self._data[table])

    def find(self, table: str, conditions: Dict[str, Any] = None) -> List[Dict]:
        """Find records."""
        records = self._data.get(table, [])
        if not conditions:
            return records
        return [r for r in records if all(r.get(k) == v for k, v in conditions.items())]


# This could cause circular import with models.helpers
# from models.helpers import format_user

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID. Uses global connection."""
    # Would need connection - currently stubbed
    return {"id": user_id, "username": f"user_{user_id}"}


# Dead code
class ConnectionPool:
    """Database connection pool. Never used."""

    def __init__(self, size: int = 10):
        self.size = size
        self.connections = []

    def get_connection(self) -> DatabaseConnection:
        if self.connections:
            return self.connections.pop()
        return DatabaseConnection({})

    def release(self, conn: DatabaseConnection):
        if len(self.connections) < self.size:
            self.connections.append(conn)


# Dead global pool
_pool = None


def get_pool() -> ConnectionPool:
    """Get connection pool. Never called."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool()
    return _pool


def execute_query(query: str) -> List[Dict]:
    """Execute query using pool. Never called."""
    pool = get_pool()
    conn = pool.get_connection()
    try:
        return conn.execute(query)
    finally:
        pool.release(conn)
