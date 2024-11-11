from influxdb_client import Point
from databases.influxdb_tools import InfluxTools
from models.notification import NotificationLog


class NotificationLogger:

    def write_state(self, notification: NotificationLog):
        """
        Write data from a otification instance to an InfluxDB bucket.
        The bucket name is expected to be the `guid` of the NotificationLog.
        """
        if not notification.guid:
            raise ValueError(
                "NotificationLog must have a guid to define the target bucket."
            )

        point = (
            Point("notification")
            .tag("name", notification.guid if notification.guid else None)
            .tag("code", notification.code if notification.code else None)
            .tag("status", notification.status if notification.status else None)
            .field("message", notification.message if notification.message else None)
            .field("state", notification.state if notification.state else None)
            .time(notification.time_stamp)
        )

        bucket_name = str(notification.guid)
        InfluxTools.write_data(bucket=bucket_name, point=point)
