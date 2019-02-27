from typing import Tuple
from logging import RootLogger


class MenuElement:
    def __init__(self, id_: str, logger: RootLogger = None):
        self._id = id_
        self._logger = logger

    def _log(self, lvl: int, msg: str):
        if self._logger:
            self._logger.log(lvl, msg)

    @classmethod
    def _from_attribs(cls, d: dict):
        c = cls("")
        c.__dict__ = d
        return c

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _):
        errormsg = "<MenuElement>.id is a read-only attribute"
        raise AttributeError(errormsg)

    def get_data(self) -> Tuple[type, dict]:
        return (MenuElement, self.__dict__)
