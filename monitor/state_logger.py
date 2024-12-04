"""State logging to influx class and method ."""

from influxdb_client import Point
from databases.influxdb_tools import InfluxTools
from models.service_state import StateLog


class Loggers:
    """
    A class to write state logs to an InfluxDB bucket.
    """

    def write_state(self, state_log: StateLog):
        """
        Write data from a StateLog instance to an InfluxDB bucket.
        """

        point = (
            Point("service_state_log")
            .tag("name", state_log.name)
            .tag("status", state_log.status)
            .tag("code", state_log.code)
            .tag("message", state_log.message)
            .field("state", state_log.state)
        )

        bucket_name = str(state_log.guid)
        InfluxTools.write_data(bucket=bucket_name, point=point)
