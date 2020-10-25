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

from osw.Frame import Frame
from osw.FrameBuilder import build_frame_ack
from osw.FrameCounter import FrameCounter
from osw.Spooler import Spooler
from osw.Storage import Storage


streamer = Streamer()
storage = Storage()
counter = FrameCounter()
spooler = Spooler(streamer, counter)
receiver = FrameReceiver(storage, spooler)
sender = FrameSender(storage, spooler, counter)


def set_initial_values():
    values = [
        (b'\x13', b'\x32', b'\x23'),
        (b'\x13', b'\x40', b'\xff'),
        (b'\x13', b'\x44', b'\xf0'),
        (b'\x13', b'\x43', b'\x0f'),
        (b'\x13', b'\x75', b'\xf0'),
        (b'\x13', b'\x76', b'\x44'),
        (b'\x13', b'\x77', b'\x44\x00'),
        (b'\x13', b'\x78', b'\x50\x00'),

        (b'\x14', b'\x32', b'\xfe\x00'),
        (b'\x14', b'\xf6', b'\xfe\x00'),
        (b'\x14', b'\xf4', b'\x15\x02\x24'),
        (b'\x14', b'\xf3', b'\x13\x07\x09'),
        (b'\x14', b'\xf5', b'\x05'),
        (b'\x14', b'\x39', b'\xd0\xb8'),
        (b'\x14', b'\xe0', b'\xfe\x00\x00\x00'),
        (b'\x14', b'\xe4', b'\x00\x04\x0d\xcb'),
        (b'\x14', b'\xe8', b'\xfe'),
        (b'\x14', b'\xe9', b'\x04'),
        (b'\x14', b'\xe6', b'\x27\x10'),

        (b'\x12', b'\x02', b'\xf0'),
        (b'\x12', b'\x41', b'\x32'),
        (b'\x12', b'\x43', b'\xe2'),
        (b'\x12', b'\x44', b'\x12'),
        (b'\x12', b'\x62', b'\x00'),
        (b'\x12', b'\x63', b'\xc2'),
        (b'\x12', b'\xea', b'\xfe'),
        (b'\x12', b'\x5a', b'\x15'),
        (b'\x12', b'\x5c', b'\x17'),
        (b'\x12', b'\x73', b'\x00'),
        (b'\x12', b'\xf7', b'\x00\x00\x00\x00'),
    ]
    for val in values:
        storage.set(val[0], val[1], val[2])

async def main():
    print('Hello World')
    set_initial_values()

    asyncio.create_task(spooler.process())
    asyncio.create_task(receiver.process())
    await streamer.serve(receiver)
    asyncio.create_task(sender.process_server())

    return start_web(storage)
    # while True:
    #     await asyncio.sleep(1)


def test():
    print('Hello Test')
    raw = 'd0c00212000000000000fe12040601010f7401f064e0'
    frame = Frame(raw)
    resp = build_frame_ack(frame)
    print(frame)
    print(resp)


if __name__ == "__main__":
    # execute only if run as a script
    # main()
    try:
        # asyncio.run(main())
        web.run_app(main(), port=5051)
    except KeyboardInterrupt:
        pass
    # test()
# 0xd00xc00x020x120x000x000x000x000x000x000xfe0x120x040x060x010x010x0f0x740x010xf00x640xe0
# d0c0 0212 0000 0000 0000 fe12 0406 0101 0f74 01f0 64e0