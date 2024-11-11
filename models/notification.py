from enums.sentinel_enums import Codes


class NotificationLog:
    def __init__(self):
        self._guid = None
        self._time_stamp = None
        self._message = None
        self._code = None
        self._user = None

    def validate(self, value, enum_class):
        if isinstance(value, enum_class):
            return value

    def set(self, guid, time_stamp=None, message=None, code=None, user=None):
        if guid:
            self._guid = guid
        if time_stamp:
            self._time_stamp = time_stamp
        if message:
            self._message = message
        if code:
            self._code = self.validate(code, Codes)
        if user:
            self._user = user

    def get(self):
        result = {
            "guid": self._guid,
            "time_stamp": self._time_stamp,
            "message": self._message,
            "code": self._code,
            "user": self._user,
        }

        return result

    # guid property
    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, value):
        self._guid = value

    # time_stamp property
    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self._time_stamp = value

    # message property
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    # code property
    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.validate(value, Codes)

    # user property
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value
