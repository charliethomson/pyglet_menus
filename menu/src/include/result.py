class ResultError(Exception):
    pass

class Result:
    def __init__(self, ok: bool, err: str="", res = None):
        self.name = "Ok" if ok else "Err"
        self.err = None if ok else err
        self.res = res if res and ok else None

    @classmethod
    def Ok(cls, res=None):
        return cls(True, res=res)

    @classmethod
    def Err(cls, err: str):
        return cls(False, err=err)

    def unwrap(self):
        if self.name == "Ok":
            return self.res
        elif self.name == "Err":
            errormsg = f"Tried to unwrap on Err variant: err={self.err}" 
            raise ResultError(errormsg)

    def is_ok(self) -> bool:
        return self.name == "Ok"

    def is_err(self) -> bool:
        return self.name == "Err"
 