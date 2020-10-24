#!/usr/bin/env python
# -*- coding: utf-8 -*-
from binascii import hexlify

from aiohttp import web

from osw.FrameReceiver import FrameReceiver
from osw.Streamer import Streamer
from osw.Webserver import start_web

try:
    import asyncio
except:
    import uasyncio as asyncio

from osw.FrameBuilder import build_frame
from osw.FrameCounter import FrameCounter
from osw.Spooler import Spooler
from osw.Storage import Storage

storage = Storage()
streamer = Streamer()
counter = FrameCounter()
spooler = Spooler(streamer, counter)
receiver = FrameReceiver(storage, spooler)


def send_init():
    build_frame(spooler, storage, counter, b'\x12\x04', (b'\x01', b'\x74'))
    build_frame(spooler, storage, counter, b'\x14\x04', (b'\x17', b'\x18', b'\x19', b'\xfd'))
    build_frame(spooler, storage, counter, b'\x14\x04', (b'\xfa', b'\xfb', b'\xfc', b'\xf7', b'\xf8', b'\xf9'))
    build_frame(spooler, storage, counter, b'\x13\x02', (b'\x32', b'\x40', b'\x44', b'\x43', b'\x75', b'\x76', b'\x77', b'\x78'))
    build_frame(spooler, storage, counter, b'\x14\x02', (b'\x32', b'\xf6', b'\xf4', b'\xf3', b'\xf5', b'\x39', b'\xe0', b'\xe4', b'\xe8', b'\xe9', b'\xe6'))
    build_frame(spooler, storage, counter, b'\x14\x04', (b'\x37', ))
    build_frame(spooler, storage, counter, b'\x14\x04', (b'\x38', ))


async def main():
    print('Hello World')
    await streamer.connect()

    asyncio.create_task(spooler.process())
    asyncio.create_task(receiver.process(streamer))

    send_init()
    return start_web(storage)
    # while True:
    #     await asyncio.sleep(1)


if __name__ == "__main__":
    # execute only if run as a script
    try:
        web.run_app(main(), port=5050)
    except KeyboardInterrupt:
        pass

# 0xd00xc00x020x120x000x000x000x000x000x000xfe0x120x040x060x010x010x0f0x740x010xf00x640xe0
# d0c0 0212 0000 0000 0000 fe12 0406 0101 0f74 01f0 64e0
