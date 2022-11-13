import json, os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'tim-eu.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'latte'

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorisation header is missing"
            }, 401)
    auth_section = auth.split()
    if auth_section[0] != "Bearer": # auth header has no Bearer prefix
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorisation header needs to include Bearer prefix"
            }, 401)
    elif len(auth_section) == 1:   # auth header has only one section
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Token missing in authorisation header"
            }, 401)
    elif len(auth_section) > 2:   # auth header has too many sections
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorisation header has too many sections"
            }, 401)

    token = auth_section[1]
    return token

def check_permissions(permission, payload):
    try:
        permissions = payload.get('permissions')
        if (permission in permissions):
            print (str(permission) + " in " + str(permissions))
            return True
        else:
            raise AuthError(
                    {
                        'code': 'invalid_permissions',
                        'description': 'User doesn\'t have permission.'
                    }, 403)
    except:
        raise AuthError(
                {
                    'code': 'invalid_permissions',
                    'description': 'User doesn\'t have permission.'
                }, 401)


def verify_decode_jwt(token):
    jsonURL = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonWebKeySet = json.loads(jsonURL.read())
    unverified_token_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_token_header:
        raise AuthError(
            {
                'code': 'invalid_token',
                'description': 'Token does not contain a Key ID (kid) and so cannot be verified.'
            }, 401)
    for key in jsonWebKeySet['keys']:
        if key['kid'] == unverified_token_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n':   key['n'],
                'e':   key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'The token has expired and can no longer be used.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code': 'invalid_token',
                    'description': 'There is a problem with the claims.'
                }, 401)
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_token',
                    'description': 'Unable to parse authentication token.'
                }, 400)


def RequiresAuth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator