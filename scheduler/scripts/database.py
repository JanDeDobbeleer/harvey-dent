import sys
import os
from influxdb import InfluxDBClient


def write_point(measurement, value, timestamp):
    try:
        client = InfluxDBClient(os.environ.get('INFLUX_URI'), os.environ.get('INFLUX_PORT'), os.environ.get(
            'INFLUX_USER'), os.environ.get('INFLUX_USER_PASSWORD'), os.environ.get('INFLUX_DB'))
        json_body = [
            {
                "measurement": measurement,
                "time": timestamp,
                "fields": {
                    "value": value
                }
            }
        ]
        client.write_points(json_body)
    except Exception as e:
        print(e)
        sys.exit(5)
