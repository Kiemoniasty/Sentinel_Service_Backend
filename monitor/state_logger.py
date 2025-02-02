"""State logging to influx class and method ."""

from datetime import datetime
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

    @staticmethod
    def query_states(guid: str, sort: str):
        """
        Query the state logs for a service from the InfluxDB bucket.
        """

        bucket_name = str(guid)
        data = InfluxTools.query_data(bucket=bucket_name)
        sorted_data = sorted(
            data,
            key=lambda x: datetime.strptime(x["time_stamp"], "%Y-%m-%dT%H:%M:%S"),
            reverse=True if sort == "desc" else False,
        )
        return sorted_data
