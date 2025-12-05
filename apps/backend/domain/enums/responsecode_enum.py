from enum import IntEnum


class ResponseCode(IntEnum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    RATE_LIMIT_EXCEEDED = 429
    SERVER_ERROR = 500
