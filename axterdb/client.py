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

class Client():
    def __init__(self, *, name: str, key: str, host: str, show_keys: bool = False):
        super().__init__()

        self.name: str = name
        self.key: str = key
        self.host: str = host
        self.show_keys: bool = show_keys
    
        self._headers: dict = {"KEY": f"{self.key}"}
        self._session: aiohttp.ClientSession = None
        self._connected: bool = False
        self._accepted_types = ["TEXT", "INT", "REAL", "NULL"]


    async def connect(self):
        """|coro|

        Connects to the database, checks if everything is correct.

        """
        logger.log(logging.INFO, "Connection to database started.")
        self._session = aiohttp.ClientSession()
        await self._check_instance()
        await self._check_access()
        atexit.register(self._close)
        self._connected = True
        logger.log(logging.INFO, "Database connection established")


    def route(self, path: str = "") -> str:
        return f"http://{self.host}{path}"


    async def _check_instance(self) -> None:
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
        logger.log(logging.INFO, "Checking instance.")
        if self._connected:
            raise AlreadyConnected(self.host, self.key, self.table, self.show_keys)            
        try:
            ip = self.host.split(":")[0]
            ipaddress.ip_address(ip)
        except ValueError:
            raise InvalidInstanceIP(self.host)
        
        try:
            async with self._session.get(self.route("/")) as response:
                if response.status != 200:
                    raise ConnectionFailure(self.host, self.key, self.show_keys)
        except ClientConnectionError as e:
            raise ConnectionFailure(self.host, self.key, self.show_keys)
        logger.log(logging.INFO, "Instance checked")

    async def _check_access(self) -> None:
        """|coro|

        Checks if the specified key has access to the specified database.

        Raises
        ------
        NoAccess
            Key specified does not have access to the specified database
        AlreadyConnected
            Already connected to the specified database.
        """
        logger.log(logging.INFO, f"Checking access for key {self.key} to {self.name}")
        if self._connected:
            raise AlreadyConnected(self.host, self.key, self.table, self.show_keys)
        async with self._session.get(self.route(f"/me"), headers=self._headers) as response:
            if response.status == 200:
                data = await response.json()
                databases = data["detail"]["data"]["Databases"]
                if self.name not in databases:
                    raise NoAccess(self.host, self.key, self.name, self.show_keys)
                else:
                    print(f"Connected to {self.name}! (Instance: {self.host} | Key: {self.key if self.show_keys else '[HIDDEN]'})")
            else:
                raise InvalidKey()
            
    async def create_table(self, table: str, **columns) -> None:
        """|coro|
        Creates a table on the database

        Parameters
        ----------
        table: :class:`str`
            The table name to create.
        **columns
            Additional arguments are used as columns for the table.

            
        Returns
        -------
        :class:`bool`
            Returns `True` if function was executed sucessfully. 

        Raises
        ------
        NotConnected
            Not connected to the database.
        UnAcceptedType
            Invalid row type.
        InvalidTable
            Table not provided.
        InvalidRows
            Rows not provided.
        TableAlreadyExists
            Table with that name already exists.
        """
        if not self._connected:
            raise NotConnected()
        columns_dict = columns
        for key in columns_dict:
            if columns_dict[key].upper() not in self._accepted_types:
                raise UnAcceptedType(columns_dict[key].upper())
        async with self._session.post(self.route(f"/database/{self.name}/create?table={table}"), headers=self._headers, json=columns_dict) as response:
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

    async def get(self, table: str, amount: str = None, **kwargs) -> list:
        """|coro|
        Get data from a table

        Parameters
        ----------
        table: :class:`str`
            The table to get data from.
        amount: :class:`str`
            The amount of data to get.
        **kwargs
            Additional arguments are used as condition arguments (WHERE in SQL)  
            
        Returns
        -------
        :class:`list`
            Returns a list of lists containing data, or an empty list if no data was found.

        Raises
        ------
        NotConnected
            Not connected to the database.
        """
        if not self._connected:
            raise NotConnected()
        data = kwargs
        headers = self._headers
        headers["table"] = table
        if amount: headers["amount"] = amount 
        async with self._session.get(self.route(f"/database/{self.name}/select"), headers=headers, json=data) as response:
            if response.status == 200:
                data = await response.json()
                rows = data["detail"]["rows"]
                return rows
            # TODO: Add errors for this
            
    async def insert(self, table: str, **data) -> bool:
        """|coro|
        Insert data into a table

        Parameters
        ----------
        table: :class:`str`
            The table to insert data to.
        **data
            Additional arguments are used as data to insert. 
            
        Returns
        -------
        :class:`bool`
            Returns True if query executed sucessfully.

        Raises
        ------
        NotConnected
            Not connected to the database.
        InvalidColumn
            Invalid column provided.
        """
        if not self._connected:
            raise NotConnected()
        data = data
        headers = self.headers
        headers["table"] = table
        async with self._session.get(self.route(f"/database/{self.name}/insert"), headers=self.headers, json=data) as response:
            if response.status == 200:
                return True
            elif response.status == 422:
                data = await response.json()
                raise InvalidColumn(data["detail"].split(' ').pop(0))
            # TODO: Add errors from status codes.

    async def get_all_tables(self) -> None:
        """|coro|
        Get all tables of the database
            
        Returns
        -------
        :class:`list`
            Returns a list of table names

        Raises
        ------
        NotConnected
            Not connected to the database.
        InvalidKey
            Key is invalid.
        """
        if not self._connected:
            raise NotConnected()
        async with self._session.get(self.route(f"/database/{self.name}/get"), headers=self._headers) as response:
            if response.status == 200:
                data = await response.json()
                tables = data["detail"]["tables"]
                return tables
            elif response.status == 401:
                raise InvalidKey()
            # TODO: Add errors from status codes.

    async def check_table(self, table: str) -> None:
        """|coro|
        Check if a table exists
            
        Parameters
        ----------

        table: :class:`str`

        Returns
        -------
        :class:`bool`
            Returns True if table exists, else False

        Raises
        ------
        NotConnected
            Not connected to the database.
        InvalidKey
            Key is invalid.
        """
        if not self._connected:
            raise NotConnected()
        async with self._session.get(self.route(f"/database/{self.name}/get?table={table}"), headers=self._headers) as response:
            if response.status == 200:
                return True
            elif response.status == 404:
                return False
            elif response.status == 401:
                raise InvalidKey()
            # TODO: Add errors from status codes.

    def _close(self) -> None:
        asyncio.run(self._session.close())