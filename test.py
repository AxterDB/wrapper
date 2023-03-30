from axterdb import AxterDBClient
import asyncio

client = AxterDBClient(name="neil", key="4bh9CQjezCsE8NJu", host="127.0.0.1:5000", show_keys=True)

async def test():
    await client.connect()

asyncio.run(test())


from discord.ext import commands


commands.Bot().run()