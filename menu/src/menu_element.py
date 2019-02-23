class MenuElement:
    def __init__(self, id_):
        self._id = id_

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _):
        raise AttributeError("<MenuElement>.id is a read-only attribute")
