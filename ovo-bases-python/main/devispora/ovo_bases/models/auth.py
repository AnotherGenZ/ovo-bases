from enum import Enum


class AuthAudience(str, Enum):
    POG = 'POG'
    OvO = 'OvO'
    Admin = 'Admin'

    def __getstate__(self):
        """Allows JsonPickle just to retrieve the value"""
        return self.value


class Auth:
    def __init__(self, client: AuthAudience, token_id: str):
        self.client = client
        self.token_id = token_id
