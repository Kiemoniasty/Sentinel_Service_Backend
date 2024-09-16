"""Model for user instance"""


class User:
    """Model for user instance"""

    def __init__(
        self, guid, login, email, password, phone_number, account_type, is_active
    ):
        self.guid = guid
        self.login = login
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.account_type = account_type
        self.is_active = is_active
