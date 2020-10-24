#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osw.FrameReceiver import FrameReceiver
from osw.Streamer import Streamer

try:
    import asyncio
except:
    import uasyncio as asyncio

import osw
from osw.Frame import Frame
from osw.FrameBuilder import build_frame_ack
from osw.FrameCounter import FrameCounter
from osw.Spooler import Spooler
from osw.Storage import Storage


streamer = Streamer()


async def main():
    print('Hello World')
    await streamer.serve()

    # asyncio.create_task(spooler.process())
    # asyncio.create_task(receiver.process())

    while True:
        await asyncio.sleep(1)


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
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    # test()
# 0xd00xc00x020x120x000x000x000x000x000x000xfe0x120x040x060x010x010x0f0x740x010xf00x640xe0
# d0c0 0212 0000 0000 0000 fe12 0406 0101 0f74 01f0 64e0