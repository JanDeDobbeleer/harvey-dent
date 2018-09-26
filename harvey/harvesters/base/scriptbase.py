import abc
import datetime
import os
from typing import Dict, Optional
from influxdb import InfluxDBClient


class ScriptBase(object):

    """The base script implementation containing all you need."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self) -> None:
        """Retrieve data from the settings source and run the data retrieval"""
        return

    def _get_timestamp(self) -> str:
        date = datetime.datetime.utcnow()
        return date.strftime('%Y-%m-%d %H:%M:%SZ')

    def _write_point(self, key: str, value: str, timestamp: str, tags: Optional[Dict]) -> None:
        """Write the values to the Carbon data store"""
        try:
            json_body = [
                {
                    "measurement": key,
                    "tags": tags,
                    "time": timestamp,
                    "fields": {
                        "value": value
                    }
                }
            ]
            client = InfluxDBClient(os.environ.get('INFLUXDB_SERVER'),
                                    os.environ.get('INFLUXDB_PORT'),
                                    os.environ.get('INFLUXDB_USER'),
                                    os.environ.get('INFLUXDB_USER_PASSWORD'),
                                    os.environ.get('INFLUXDB_DB'))
            client.write_points(json_body)
            print("Inserted value {} for key {}".format(value, key))
        except ConnectionError as e:
            print("Can't connect to the database...")
            raise e
