import abc
from typing import Dict
from .scriptbase import ScriptBase


class MultiPointsBase(ScriptBase):

    """The base script implementation containing all you need."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__()
        self.settings = settings
        self.config = config

    @abc.abstractmethod
    def get_data(self, key_value: str) -> Dict:
        """get key from the settings source and run the data retrieval"""
        return dict()

    @abc.abstractmethod
    def get_description(self) -> str:
        """get key from the settings source and run the data retrieval"""
        return "Dict script base running"

    def _write_points(self, key: str, details: Dict, timestamp: str) -> None:
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            super()._write_point(point, value, timestamp, None)

    def run(self) -> None:
        try:
            print(self.get_description())
            timestamp = super()._get_timestamp()
            for (key, value) in self.settings.items():
                details = self.get_data(value)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)
