import os
from typing import Any, Dict

import jwt
from jwt.exceptions import DecodeError, InvalidAudienceError

from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.auth import AuthAudience

SECRET = os.environ['JWT_SECRET']


def validate_jwt(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS512'], audience=[
                             AuthAudience.POG, AuthAudience.OvO, AuthAudience.Admin])

        return payload
    except InvalidAudienceError:
        raise RequestException(
            message=RequestExceptionMessage.InvalidAuthAudience)
    except DecodeError:
        raise RequestException(
            message=RequestExceptionMessage.CannotValidateAuthToken)
