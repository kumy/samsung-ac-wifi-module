# -*- coding: utf-8 -*-
from osw.Webserver import start_web

try:
    import asyncio
except:
    import uasyncio as asyncio


class Streamer:
    spooler = None
    _sreader = None
    _swriter = None

    is_server = None

    async def read(self):
        if self._sreader is None or self._sreader.at_eof():
            if self.is_server:
                print('D: Streamer: Client disconnected! - DEBUG 1')
                # raise Exception
                return False
            await self.connect()
            return

        return await self._sreader.read(1)

    async def write(self, data):
        if self._swriter is None:
            return False

        try:
            self._swriter.write(data)
            await self._swriter.drain()
        except:
            if self.is_server:
                print('D: Streamer: Client disconnected! - DEBUG 2')
            else:
                await self.connect()
            return False
        return True

    async def connect(self):
        self.is_server = False
        print('D: Streamer.connect()')
        try:
            self._sreader, self._swriter = await asyncio.open_connection('127.0.0.1', 8888)
            print('D: Streamer: connected!')
        except:
            print('D: Streamer still not connected')
            # await asyncio.sleep(1)
            # pass

    async def serve(self, receiver):
        self.is_server = True

        async def client_connected_cb(reader, writer):
            print('D: Streamer: Client connected!')
            self._sreader, self._swriter = (reader, writer)
            receiver.streamer = self

        await asyncio.start_server(client_connected_cb, port=8888)
        print('D: Streamer: Listening connections!')
