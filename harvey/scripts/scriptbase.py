import abc
import os
import time
import graphitesend

class ScriptBase(object):
    """The base script implementation containing all you need."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        """Retrieve data from the settings source and run the data retrieval"""
        return

    def _get_timestamp(self):
        return int(time.time())

    def _write_point(self, measurement, value, timestamp):
        """Write the values to the Carbon data store"""
        try:
            graphitesend.init(graphite_server=os.environ.get('GRAPHITE_SERVER'),
                              graphite_port=int(os.environ.get('GRAPHITE_PORT')),
                              prefix=os.environ.get('GRAPHITE_PREFIX'),
                              system_name=os.environ.get('GRAPHITE_NAME'))
            graphitesend.send(measurement, value, timestamp)
            graphitesend.reset()
        except ConnectionError as error:
            print("Can't connect to the database...")

