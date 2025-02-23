"""Collection of functions to check the health of a service."""

import subprocess
from databases.postgres_tools import PostgresTools
from enums.sentinel_enums import Codes, Response
from models.service_state import StateLog
from monitor.state_logger import StateLogger


class HealthChecker:
    """HealthChecker class to check the health of a service."""

    def ping_service(self=None, guid=None, service=None, settings=None):
        """
        Ping a service to check its reachability.

        Args:
        - address (str): IP address or hostname of the service.
        """
        data = {}
        state_log = StateLog()
        state_log.guid = service.guid
        state_log.name = service.name

        try:
            # Use subprocess to send ping command
            subprocess.run(
                [
                    "ping",
                    "-c",
                    str(settings.number_of_samples),
                    "-W",
                    str(settings.response_time),
                    settings.address,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            state_log.state = Response.AVAILABLE.value
            state_log.message = Codes.I004.value
            state_log.code = Codes.I004.name
            state_log.status = settings.status.value

            data["actual_state"] = Response.AVAILABLE.name

        # If the ping command returns 0, the service is reachable
        except subprocess.CalledProcessError:

            state_log.state = Response.UNAVAILABLE.value
            state_log.message = Codes.E001.value
            state_log.code = Codes.E001.name
            state_log.status = settings.status.value

            data["actual_state"] = Response.UNAVAILABLE.name

        PostgresTools.update_service(guid=guid, data=data)

        StateLogger.write_state(None, state_log)
