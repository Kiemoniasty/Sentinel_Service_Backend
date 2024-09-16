from models.settings import Settings


class Service:

    def __init__(self, guid, name, setting_guid, actual_state=None):
        self.guid = guid
        self.name = name
        self.setting_guid = setting_guid
        self.actual_state = actual_state
        Settings(setting_guid, None, None, None, None, None)
