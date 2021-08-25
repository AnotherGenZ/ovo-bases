from enum import Enum


class AuthAudience(str, Enum):
    POG = 'POG'
    OvO = 'OvO'
    Admin = 'Admin'


class Auth:
    def __init__(self, client: AuthAudience):
        self.client = client
