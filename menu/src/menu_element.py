from typing import Tuple, Optional, Any
from logging import RootLogger, INFO, ERROR, WARNING
from .include.result import Result


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

    def update_data(self, item: Tuple[str, Any]) -> Result:
        key, value = item
        if not key.startswith("_"):
            errormsg = f"{key} doesn't seem to belong"
            self._log(WARNING, errormsg)
            return Result.Err(errormsg)
        else:
            key = key[1:]

        if key in self.__dict__:
            old = self.__dict__[key]
            self._log(INFO, f"MenuElement.update_data called with {item}; setting existing value {old} to {value}")
            self.__dict__[key] = value
            return Result.Ok(old)
        else:
            self._log(ERROR, f"MenuElement.update_data called with {item}; ADDING VALUE {key} -> {value}")
            self.__dict__[key] = value
            return Result.Ok()