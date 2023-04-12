import axterdb
import asyncio

client = axterdb.Client(name="db name", key="key here", host="instance IP")

async def main():
    client.connect()
    client.create_table(table="test", row1="text", row2="text")
    client.insert(table="test", row1="text 1", row2="text 2")
    client.insert(table="test", row1="text 3", row2="text4")
    client.get(table="test") # no filter
    client.get(table="test", amount=1) # filter by amount
    client.get(table="test", row1="text 1") # filter by value

asyncio.run(main())