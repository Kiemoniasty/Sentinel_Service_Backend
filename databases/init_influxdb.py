from databases.influxdb_tools import InfluxTools


class InitInfluxDB:

    @staticmethod
    def create_logs_bucket():
        """
        Query all buckets and create app_logs bucket if it does not exist.
        """
        client = InfluxTools.connector()
        buckets_api = client.buckets_api()
        all_buckets = buckets_api.find_buckets().buckets
        is_exist = False
        for bucket in all_buckets:
            bucket_name = bucket.name
            if bucket_name == "app_logs":
                is_exist = True
                break

        if not is_exist:
            InfluxTools.create_bucket(name="app_logs")
