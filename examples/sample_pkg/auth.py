from .store import SessionStore


class AuthService:
    def __init__(self) -> None:
        self.store = SessionStore()

    def login(self, user: str) -> str:
        return self.store.get(user)
