"""Collection of setters/getter for StateLog model"""


class StateLog:
    """StateLog model for influxdb"""

    def __init__(self):
        self._guid = None
        self._time_stamp = None
        self._name = None
        self._state = None
        self._message = None
        self._code = None
        self._status = None

    def set(
        self,
        guid,
        time_stamp=None,
        name=None,
        state=None,
        message=None,
        code=None,
        status=None,
    ):
        """Massive setter method"""
        if guid:
            self._guid = guid
        if time_stamp:
            self._time_stamp = time_stamp
        if name:
            self._name = name
        if state:
            self._state = state
        if message:
            self._message = message
        if code:
            self._code = code
        if status:
            self._status = status

    def get(self):
        """Get values for instance of StateLog"""
        result = {
            "guid": self._guid,
            "time_stamp": (
                self._time_stamp.strftime("%Y-%m-%dT%H:%M:%S")
                if self._time_stamp
                else None
            ),
            "name": self._name,
            "state": self._state,
            "message": self._message,
            "code": self._code,
            "status": self._status,
        }

        return result

    @property
    def guid(self):
        """Get GUID of StateLog instance"""
        return self._guid

    @guid.setter
    def guid(self, value):
        """Set GUID for StateLog instance"""
        self._guid = value

    @property
    def time_stamp(self):
        """Get time_stamp of StateLog instance"""
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        """Set timestamp for StateLog instance"""
        self._time_stamp = value

    @property
    def name(self):
        """Get name of StateLog instance"""
        return self._name

    @name.setter
    def name(self, value):
        """Set name for StateLog instance"""
        self._name = value

    @property
    def state(self):
        """Get state of StateLog instance"""
        return self._state

    @state.setter
    def state(self, value):
        """Set state for StateLog instance"""
        self._state = value

    @property
    def message(self):
        """Get message of StateLog instance"""
        return self._message

    @message.setter
    def message(self, value):
        """Set message for StateLog instance"""
        self._message = value

    @property
    def code(self):
        """Get code of StateLog instance"""
        return self._code

    @code.setter
    def code(self, value):
        """Set code for StateLog instance"""
        self._code = value

    @property
    def status(self):
        """Get status of StateLog instance"""
        return self._status

    @status.setter
    def status(self, value):
        """Set status for StateLog instance"""
        self._status = value
