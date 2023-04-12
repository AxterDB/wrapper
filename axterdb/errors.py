class ConnectionFailure(Exception):
    def __init__(self, host: str, key: str, show_keys: bool = False):
        self.host = host
        self.key = key 
        super().__init__(f"Failed connecting to {self.host} with key {self.key if show_keys else '[HIDDEN]'}")

class NoAccess(Exception):
    def __init__(self, host: str, key: str, table: str, show_keys: bool = False):
        self.host = host
        self.key = key
        self.table = table
        super().__init__(f"You don't have access to {self.table} table! (Instance: {self.host} | Key: {self.key if show_keys else '[HIDDEN]'})")

class InvalidKey(Exception):
    def __init__(self):
        super().__init__("Specified key is invalid.")

class InvalidInstanceIP(Exception):
    def __init__(self, host: str):
        self.host = host
        super().__init__(f"{self.host} is not a valid instance IP")

class AlreadyConnected(Exception):
    def __init__(self, host: str, key: str, table: str, show_keys: bool = False):
        self.host = host
        self.key = key
        self.table = table
        super().__init__(f"You are already connected to {self.table}! (Instance: {self.host} | Key: {self.key if show_keys else '[HIDDEN]'})")

class NotConnected(Exception):
    def __init__(self):
        super().__init__("You aren't connected to the database!")

class UnAcceptedType(Exception):
    def __init__(self, type: str):
        self.type = type
        super().__init__(f"{self.type} is not a accepted type!")

class TableAlreadyExists(Exception):
    def __init__(self, table: str):
        self.table = table
        super().__init__(f"{self.table} already exists!")

class InvalidTable(Exception):
    def __init__(self):
        super().__init__("Table is an argument that's missing")

class InvalidRows(Exception):
    def __init__(self):
        super().__init__("Rows is an argument that's missing")

class InvalidColumn(Exception):
    def __init__(self, column: str):
        self.column = column
        super().__init__(f"{self.column} is not a column in the table!")

class UnknownError(Exception):
    def __init__(self, status_code):
        super().__init__(f"There was an error while trying to perform this action, if you see this, please report this issue!\nSTATUS CODE: {status_code}")