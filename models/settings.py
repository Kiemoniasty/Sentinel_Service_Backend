class Settings:

    def __init__(
        self, guid, status, address, frequency, response_time, number_of_samples
    ):
        self.guid = guid
        self.status = status
        self.address = address
        self.frequency = frequency
        self.response_time = response_time
        self.number_of_samples = number_of_samples
