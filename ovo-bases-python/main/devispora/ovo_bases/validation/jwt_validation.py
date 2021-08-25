import os
from typing import Any

import jwt
from jwt.exceptions import DecodeError, InvalidAudienceError

from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.auth import AuthAudience


def validate_jwt(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS512'], audience=[
                             AuthAudience.POG, AuthAudience.OvO, AuthAudience.Admin])

        return payload
    except InvalidAudienceError as error:
        raise RequestException(
            message=RequestExceptionMessage.InvalidAuthAudience)
    except DecodeError as error:
        raise RequestException(
            message=RequestExceptionMessage.CannotValidateAuthToken)
