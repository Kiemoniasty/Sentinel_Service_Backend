"""Influxdb tools that can be used in none specific tasks"""

import os
import time
from dotenv import load_dotenv
from influxdb_client import BucketRetentionRules, InfluxDBClient, Point

import constants

load_dotenv(override=True)


class InfluxTools:
    """Universal InfluxDB tools"""

    def connector(self=None):
        """Establish connection with InfluxDB"""
        influxdb_url = os.getenv("INFLUXDB_URL")
        influxdb_token = os.getenv("INFLUXDB_TOKEN")
        influxdb_org = os.getenv("INFLUXDB_ORG")

        return InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

    def create_bucket(self=None, name=None, retention=None):
        """Creates bucket in organisation"""
        client = InfluxTools.connector()

        if isinstance(retention, int) or retention == "" or retention is None:
            retention = 180 * 24 * 60 * 60
        else:
            retention = retention * 24 * 60 * 60

        retention_rules = BucketRetentionRules(type="expire", every_seconds=retention)

        client.buckets_api().create_bucket(
            bucket_name=str(name),
            retention_rules=retention_rules,
            org=os.getenv("INFLUXDB_ORG"),
        )

        client.close()

        content = constants.BKT_NEW1 + str(name) + constants.BKT_NEW2
        InfluxTools.write_log(content)

    def delete_bucket(self=None, name=None):
        """Deletes bucket in organisation"""
        client = InfluxTools.connector()

        try:
            buckets_api = client.buckets_api()
            # Get the bucket details by name
            bucket = buckets_api.find_bucket_by_name(str(name))
            if not bucket:
                print(f"Bucket '{name}' not found.")
                return
            # Delete the bucket
            buckets_api.delete_bucket(bucket)
            content = constants.BKT_DEL1 + str(name) + constants.BKT_DEL2
        except Exception as e:
            content = constants.BKT_ERROR + str(e)
        finally:
            client.close()
            InfluxTools.write_log(content)

    def write_data(self=None, bucket=None, point=None):
        """Write data to the specified bucket"""
        client = InfluxTools.connector()

        # Write the point to the specified bucket
        write_api = client.write_api()
        write_api.write(bucket=bucket, org=os.getenv("INFLUXDB_ORG"), record=point)
        client.close()

    @staticmethod
    def write_log(content):
        """Write data to the logs bucket"""
        # time.sleep(1)
        client = InfluxTools.connector()

        point = Point("app_logs").tag("log", "log").field("content", content)

        write_api = client.write_api()
        write_api.write(bucket="app_logs", org=os.getenv("INFLUXDB_ORG"), record=point)
        client.close()
