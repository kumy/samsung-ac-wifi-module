#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web

from osw.FrameReceiver import FrameReceiver
from osw.FrameSender import FrameSender
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
sender = FrameSender(storage, spooler, counter)


def set_initial_values():
    try:
        from network import WLAN
        mac = WLAN().config('mac')
        # is connected to values
    except ImportError:
        mac = bytes.fromhex('deadbeefdead')

    values = [
        (b'\x14', b'\xfa', b'\xf8'),
        (b'\x14', b'\xfb', b'\x04'),
        (b'\x14', b'\xfc', b'\x2e'),
        (b'\x14', b'\xf7', bytes([mac[3]])),
        (b'\x14', b'\xf8', bytes([mac[4]])),
        (b'\x14', b'\xf9', bytes([mac[5]])),
    ]
    for val in values:
        storage.set(val[0], val[1], val[2])

# d0c002 30 000000000015 fe 1206 24 0201f0 **410132** 4301e2 440112 620100 6301c2 **ea01fe** 5a0115 5c0117 730100 f70400000000 dc e0

async def main():
    print('Hello World')
    set_initial_values()
    await streamer.connect()

    asyncio.create_task(spooler.process())
    asyncio.create_task(receiver.process(streamer))
    asyncio.create_task(sender.process())

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
# d0c0 02 12 000000000000 fe 1204 06 01010f 7401f0 64 e0
# d0c0 02 20 000000000009 fe 1202 14 0100 0200 4300 5a00 4400 f700 5c00 7300 6200 6300 46 e0