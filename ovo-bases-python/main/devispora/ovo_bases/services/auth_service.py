from devispora.ovo_bases.validation.jwt_validation import validate_jwt
from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.responses import error_response
from devispora.ovo_bases.models.auth import Auth, AuthAudience


def retrieve_auth_details(event: dict) -> (bool, str):
    try:
        return True, event['headers']['authorization'], None
    except KeyError:
        return False, None, error_response(
            400, RequestException(RequestExceptionMessage.AuthorizationHeaderNotProvided))


def auth_request(auth_token: str) -> (bool, dict, dict):
    try:
        auth_details = validate_jwt(auth_token)
        auth = Auth(client=AuthAudience[auth_details['aud']])
        return True, auth, None
    except RequestException as error:
        return False, None, error_response(401, error)
