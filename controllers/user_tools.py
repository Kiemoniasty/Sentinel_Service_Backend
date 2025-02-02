"""Collection of tools for User Controllers"""

from enums.user_enums import AccountType
from werkzeug.security import generate_password_hash, check_password_hash


class UserTools:
    """Tools for Users Controllers"""

    def user_to_list(self=None, data=None):
        """Convert user model to a list object."""
        result = []

        for item in data:
            result.append(
                {
                    "guid": item.guid,
                    "login": item.login,
                    "email": item.email,
                    "phone_number": item.phone_number,
                    "account_type": item.account_type.value,
                    "is_active": "active" if item.is_active else "inactive",
                }
            )

        return result

    def valid_account_type(self=None, account_type=None):
        """Validate the account type."""

        for item in AccountType:
            if item.value == account_type.lower():
                return item.name

    def valid_is_active(self=None, is_active=None):
        """Validate the is_active field."""
        if str(is_active).lower() == "active" or is_active is True:
            return True
        elif str(is_active).lower() == "inactive" or is_active is False:
            return False
        else:
            return None

    def valid_new_user(self=None, data=None):
        """Validate new user data."""
        message = []

        from models.user import User

        if data.get("login"):
            query = User.query.filter_by(login=data.get("login"))
            result = UserTools.user_to_list(data=query)
            if result:
                message.append("Login")

        if data.get("email"):
            query = User.query.filter_by(email=data.get("email"))
            result = UserTools.user_to_list(data=query)
            if result:
                message.append("Email")

        if data.get("phone_number"):
            query = User.query.filter_by(phone_number=data.get("phone_number"))
            result = UserTools.user_to_list(data=query)
            if result:
                message.append("Phone number")

        if message:
            message = ", ".join(message)
            message += " already in use."

        return message

    def hash_password(self=None, password=None):
        """Hash the password"""

        return generate_password_hash(password)

    def check_password(self=None, password=None, hashed_pass=None):
        """Check the password"""

        return check_password_hash(hashed_pass, password)
