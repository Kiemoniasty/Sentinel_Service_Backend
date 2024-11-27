# from re import findall
import subprocess
from enums.sentinel_enums import Response


class HealthChecker:

    def ping_service(self, address, timeout=1, count=4):
        """
        Ping a service to check its reachability.

        Args:
        - address (str): IP address or hostname of the service.
        - timeout (int): Time in seconds to wait for each ping response.
        - count (int): Number of ping requests to send.

        Returns:
        - bool: True if the service is reachable, False otherwise.
        """

        try:
            # Use subprocess to send ping command
            subprocess.run(
                ["ping", "-c", str(count), "-W", str(timeout), address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            return Response.AVAILABLE.value
        # If the ping command returns 0, the service is reachable
        except subprocess.CalledProcessError:

            return Response.UNAVAILABLE.value
