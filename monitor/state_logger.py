from influxdb_client import Point
from databases.influxdb_tools import InfluxTools
from models.service_state import StateLog


class StateLogger:
    def write_state(self, state_log: StateLog):
        """
        Write data from a StateLog instance to an InfluxDB bucket.
        The bucket name is expected to be the `guid` of the StateLog.
        """
        if not state_log.guid:
            raise ValueError("StateLog must have a guid to define the target bucket.")

        point = (
            Point("state_log")
            .tag("code", state_log.code.value if state_log.code else None)
            .tag("status", state_log.status.value if state_log.status else None)
            .field("message", state_log.message.value if state_log.message else None)
            .field("state", state_log.state.value if state_log.state else None)
            .time(state_log.time_stamp)
        )

        bucket_name = str(state_log.guid)
        InfluxTools.write_data(bucket=bucket_name, point=point)

    # UPDATE ACTUAL STATE in Services db
