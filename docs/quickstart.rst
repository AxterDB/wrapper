:orphan:

.. _quickstart:

.. currentmodule:: axterdb

Quickstart
==========

This page gives a brief introduction to the library. It assumes you have the library installed.
If you don't, check the :ref:`installing` portion.

A Minimal Connection
--------------------

Let's connect to the database, create a table & insert data!

It looks something like this:

.. note::

    This example requires a database, key & an instance! We host a free instance, join a discord and request for a key!

.. code-block:: python3

    # This example is incomplete & is a TODO. It will be updated before release.

    import axterdb
    import asyncio

    client = axterdb.Client(name="database name here", key="your key here", host="instance ip here")

    async def main():
        await client.connect()
        await client.create_table(table="test", row1="text", row2="int", row3="real")
        await client.insert(table="test", row1="some text", row=2, row3=3.3)
        await client.get(table="test", amount=1)

    asyncio.run(main())

Let's name this file ``example_db.py``. Make sure not to name it ``axterdb.py`` as that'll conflictwith the library.

There's a lot going on here, so let's walk you through it step by step:

1. The first line just imports the library, if this raises a `ModuleNotFoundError` or `ImportError`
   then head on over to :ref:`installing` section to properly install.
2. Next, we create an instance of a :class:`Client`. This client is our connection to Discord.
3. We then create a function called `main`.
4. Now, we connect to the database using the `.connect()` method on our client instance!
5. Next, we create a table called "test" with a few rows. 
6. We then insert data into the newly made table.
7. Now, we get data from the newly made table.
.. note::
    
    While creating the table, you should know that the table only accepts `TEXT`, `INT`, `REAL` and `NULL` as a type!

Now that we've made a script, we need to run it. Since this is a simple Python script, we can run it directly.

On Windows:

.. code-block:: shell

    $ py -3 example_db.py

On other systems:

.. code-block:: shell

    $ python3 example_db.py