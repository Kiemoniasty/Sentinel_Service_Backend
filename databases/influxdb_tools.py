"""Influxdb tools that can be used in none specific tasks"""

import os
from dotenv import load_dotenv
from influxdb_client import BucketRetentionRules, InfluxDBClient

load_dotenv(override=True)


class InfluxTools:
    """Universal InfluxDB tools"""

    def influxdb_connector(self=None):
        """Establish connection with InfluxDB"""
        influxdb_url = os.getenv("INFLUXDB_URL")
        influxdb_token = os.getenv("INFLUXDB_TOKEN")
        influxdb_org = os.getenv("INFLUXDB_ORG")

        return InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

    def create_bucket(self, name, retention=None):
        """Creates bucket in organisation"""
        client = InfluxTools.influxdb_connector()

        if isinstance(retention, int) or retention == "" or retention is None:
            retention = 180 * 24 * 60 * 60
        else:
            retention = retention * 24 * 60 * 60

        retention_rules = BucketRetentionRules(type="expire", every_seconds=retention)

        return client.buckets_api().create_bucket(
            bucket_name=name,
            retention_rules=retention_rules,
            org=os.getenv("INFLUXDB_ORG"),
        )
