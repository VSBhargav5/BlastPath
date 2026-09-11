from .auth import AuthService


def handle_login(user: str) -> str:
    svc = AuthService()
    return svc.login(user)
