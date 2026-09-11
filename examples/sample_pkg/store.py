from .db import DatabasePool


class SessionStore:
    def __init__(self) -> None:
        self.pool = DatabasePool()

    def get(self, key: str) -> str:
        self.pool.acquire()
        return key
