from enum import Enum


class AccountType(Enum):
    """Enum list for column account_type in users table"""

    ADMIN = "admin"
    USER = "user"
