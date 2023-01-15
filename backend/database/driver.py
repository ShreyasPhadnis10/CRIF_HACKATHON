import zlib
from typing import Any


class Driver:
    def __init__(self):
        self._connection = None 
        self.identifier = None 

    async def connect(self, **kwargs):
        raise NotImplementedError

    async def insert(self, *args, **kwargs):
        raise NotImplementedError

    async def cleanup(self):
        raise NotImplementedError
