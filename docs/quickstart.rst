:orphan:

.. _quickstart:

.. currentmodule:: discord

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

    from axterdb import AxterDBClient
    import asyncio

    client = AxterDBClient(name="database name here", key="your key here", host="instance ip here")

    async def main():
        client.connect()

Let's name this file ``example_db.py``. Make sure not to name it ``axterdb.py`` as that'll conflictwith the library.

There's a lot going on here, so let's walk you through it step by step:

1. The first line just imports the library, if this raises a `ModuleNotFoundError` or `ImportError`
   then head on over to :ref:`installing` section to properly install.
2. Next, we create an instance of a :class:`AxterDBClient`. This client is our connection to Discord.

.. note::
    
    The steps are TODO, these will be updated before release.


Now that we've made a script, we need to run it. Since this is a simple Python script, we can run it directly.

On Windows:

.. code-block:: shell

    $ py -3 example_db.py

On other systems:

.. code-block:: shell

    $ python3 example_db.py