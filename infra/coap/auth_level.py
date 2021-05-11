from enum import Enum
class AuthLevel(Enum):
    UNAUTHENTICATED = 0
    COMPATIBLE = 1
    REGISTRED = 2
    AUTHENTICATED = 3
    