from enums.sentinel_enums import Codes, LoggerMessages, Response, Status


class StateLog:

    def __init__(self):
        self._guid = None
        self._time_stamp = None
        self._state = None
        self._message = None
        self._code = None
        self._status = None

    def validate(self, value, enum_class):
        if isinstance(value, enum_class):
            return value

    def set(
        self, guid, time_stamp=None, state=None, message=None, code=None, status=None
    ):
        if guid:
            self._guid = guid
        if time_stamp:
            self._time_stamp = time_stamp
        if state:
            self.validate(state, Response)
        if message:
            self.validate(message, LoggerMessages)
        if code:
            self.validate(code, Codes)
        if status:
            self.validate(status, Status)

    def get(self):
        result = {
            "guid": self._guid,
            "time_stamp": self._time_stamp,
            "state": self._state,
            "message": self._message,
            "code": self._code,
            "status": self._status,
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

    # state property with validation
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = self.validate(value, Response)

    # message property with validation
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = self.validate(value, LoggerMessages)

    # code property with validation
    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.validate(value, Codes)

    # status property with validation
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = self.validate(value, Status)
