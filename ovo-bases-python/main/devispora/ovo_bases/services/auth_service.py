from devispora.ovo_bases.validation.jwt_validation import validate_jwt
from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.responses import auth_response
from devispora.ovo_bases.models.auth import Auth, AuthAudience


def auth_request(auth_token: str):
    try:
        auth_details = validate_jwt(auth_token)
        auth = Auth(client=AuthAudience[auth_details['aud']])
        return (True, auth, None)
    except RequestException as error:
        return (False, None, auth_response(error))
