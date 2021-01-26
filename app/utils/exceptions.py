from typing import Dict


class MessageException(Exception):
    def __init__(self, status_code: int, content: Dict, headers: Dict = {}):
        self.status_code = status_code
        self.content = content
        self.headers = headers
