# -*- coding: utf-8 -*-

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
        # try:
        #     pass
        # except KeyboardInterrupt:
        #     return

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
            # self.spooler.set_streams(reader, writer)
            print('D: Streamer: connected!')
        except:
            print('D: Streamer still not connected')
            # await asyncio.sleep(1)
            # pass

    async def serve(self):
        self.is_server = True
        from osw.Storage import Storage
        from osw.FrameCounter import FrameCounter
        from osw.FrameReceiver import FrameReceiver
        from osw.Spooler import Spooler

        async def client_connected_cb(reader, writer):
            print('D: Streamer: Client connected!')
            self._sreader, self._swriter = (reader, writer)
            storage = Storage()
            counter = FrameCounter()
            spooler = Spooler(self, counter)
            task_spooler = asyncio.create_task(spooler.process())
            receiver = FrameReceiver(storage, spooler)
            await receiver.process(self)
            task_spooler.cancel()
            print('D: Streamer: Client connected! END')

        await asyncio.start_server(client_connected_cb, port=8888)
        print('D: Streamer: Listening connections!')
