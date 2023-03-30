from .errors import *

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
import asyncio

import ipaddress
import atexit
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('axterdb.log')
logger.addHandler(file_handler)

class AxterDBClient():
    def __init__(self, *, name: str, key: str, host: str, show_keys: bool = False):
        super().__init__()

        self.name: str = name
        self.key: str = key
        self.host: str = host
        self.show_keys: bool = show_keys
    
        self.headers: dict = {"KEY": f"{self.key}"}
        self.session: aiohttp.ClientSession = None
        self.connected: bool = False
        self.accepted_types = ["TEXT", "INT", "REAL", "NULL"]


    async def connect(self):
        """|coro|

        Connects to the database, checks if everything is correct.

        """
        logging.log(logging.INFO, "Connection to database started.")
        self.session = aiohttp.ClientSession()
        await self.check_instance()
        await self.check_access()
        atexit.register(self.close)
        self.connected = True
        logging.log(logging.INFO, "Database connection established")


    def route(self, path: str = "") -> str:
        return f"http://{self.host}{path}"


    async def check_instance(self) -> None:
        """|coro|

        Check if the IP specified is a correct instance

        Raises
        ------
        InvalidInstanceIP
            The IP provided is not an actual IP
        ConnectionFailure
            Connection to the instance failed
        AlreadyConnected
            Already connected to the specified database.
        """
        logging.log(logging.INFO, "Checking instance.")
        if self.connected:
            raise AlreadyConnected(self.host, self.key, self.table, self.show_keys)            
        try:
            ip = self.host.split(":")[0]
            ipaddress.ip_address(ip)
        except ValueError:
            raise InvalidInstanceIP(self.host)
        
        try:
            async with self.session.get(self.route("/")) as response:
                if response.status != 200:
                    raise ConnectionFailure(self.host, self.key, self.show_keys)
        except ClientConnectionError as e:
            raise ConnectionFailure(self.host, self.key, self.show_keys)
        logging.log(logging.INFO, "Instance checked")

    async def check_access(self) -> None:
        """|coro|

        Checks if the specified key has access to the specified database.

        Raises
        ------
        NoAccess
            Key specified does not have access to the specified database
        AlreadyConnected
            Already connected to the specified database.
        """
        logging.log(logging.INFO, f"Checking access for key {self.key} to {self.name}")
        if self.connected:
            raise AlreadyConnected(self.host, self.key, self.table, self.show_keys)
        async with self.session.get(self.route(f"/me"), headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                databases = data["detail"]["data"]["Databases"]
                if self.name not in databases:
                    raise NoAccess(self.host, self.key, self.name, self.show_keys)
                else:
                    print(f"Connected to {self.name}! (Instance: {self.host} | Key: {self.key if self.show_keys else '[HIDDEN]'})")
            else:
                raise InvalidKey()
            
    async def create_table(self, table: str, **rows) -> None:
        """|coro|
        Retrieves a :class:`.PartialAppInfo` from an application ID.

        Parameters
        ----------
        application_id: :class:`int`
            The application ID to retrieve information from.

        Returns
        -------
        :class:`.PartialAppInfo`
            The application information.

        Raises
        ------
        NotFound
            An application with this ID does not exist.
        HTTPException
            Retrieving the application failed.
        """
        rows_dict = rows
        for key in rows_dict:
            if rows_dict[key].upper() not in self.accepted_types:
                raise UnAcceptedType(rows_dict[key].upper())
        print(rows_dict)
        async with self.session.post(self.route(f"/database/{self.name}/create?table={table}"), headers=self.headers, json=rows_dict) as response:
            if response.status == 200:
                return True
            elif response.status == 401:
                raise InvalidKey()
            elif response.status == 422:
                data = await response.json()
                error: str = data["detail"]["message"]
                if "table" in error:
                    raise InvalidTable()
                elif "rows" in error:
                    raise InvalidRows()
            elif response.status == 409:
                raise TableAlreadyExists(table)                
            else:
                return False

    async def get(self, table: str, amount: str | None = None, **kwargs):
        if not self.connected:
            raise NotConnected()
        data = kwargs
        headers = self.headers
        headers["table"] = table
        if amount: headers["amount"] = amount 
        async with self.session.get(self.route(f"/database/{self.name}/select"), headers=headers, json=data) as response:
            if response.status == 200:
                data = await response.json()
                rows = data["detail"]["rows"]
                return rows
            
    async def insert(self, table, **data):
        if not self.connected:
            raise NotConnected()
        data = data
        headers = self.headers
        headers["table"] = table
        async with self.session.get(self.route(f"/database/{self.name}/insert"), headers=self.headers, json=data) as response:
            if response.status == 200:
                return True
            elif response.status == 422:
                data = await response.json()
                raise InvalidColumn(data["detail"].split(' ').pop(0))

    async def get_all_tables(self) -> None:
        if not self.connected:
            raise NotConnected()
        async with self.session.get(self.route(f"/database/{self.name}/get"), headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                tables = data["detail"]["tables"]
                return tables
            elif response.status == 401:
                raise InvalidKey()
            
    async def check_table(self, table: str) -> None:
        if not self.connected:
            raise NotConnected()
        async with self.session.get(self.route(f"/database/{self.name}/get?table={table}"), headers=self.headers) as response:
            if response.status == 200:
                return True
            elif response.status == 404:
                return False
            elif response.status == 401:
                raise InvalidKey()

    def close(self) -> None:
        asyncio.run(self.session.close())