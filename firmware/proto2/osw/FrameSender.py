# -*- coding: utf-8 -*-
from osw.FrameBuilder import build_frame

try:
    import asyncio
except:
    import uasyncio as asyncio


class FrameSender:
    INITIAL_VALUES = [
        # (b'\x12\x04', (b'\x01', b'\x74')),
        # (b'\x14\x04', (b'\x17', b'\x18', b'\x19', b'\xfd')),
        # (b'\x14\x04', (b'\xfa', b'\xfb', b'\xfc', b'\xf7', b'\xf8', b'\xf9')),
        # (b'\x13\x02', (b'\x32', b'\x40', b'\x44', b'\x43', b'\x75', b'\x76', b'\x77', b'\x78')),
        # (b'\x14\x02', (b'\x32', b'\xf6', b'\xf4', b'\xf3', b'\xf5', b'\x39', b'\xe0', b'\xe4', b'\xe8', b'\xe9', b'\xe6')),
        # (b'\x14\x04', (b'\x37', )),
        # (b'\x14\x04', (b'\x38', )),
        (b'\x12\x02', (b'\x01', b'\x02', b'\x43', b'\x5a', b'\x44', b'\xf7', b'\x5c', b'\x73', b'\x62', b'\x63')),
    ]
    INITIAL_SERVER_VALUES = [
        (b'\x12\x06', (b'\x02', b'\x41', b'\x43', b'\x44', b'\x62', b'\x63', b'\xea', b'\x5a', b'\x5c', b'\x73', b'\xf7')),
    ]

    def __init__(self, storage, spooler, counter):
        self.storage = storage
        self.spooler = spooler
        self.counter = counter

    async def process(self):
        for val in self.INITIAL_VALUES:
            self._send(val)

    async def process_server(self):
        await asyncio.sleep(40)
        for val in self.INITIAL_SERVER_VALUES:
            self._send(val)

    def _send(self, val):
        frame = build_frame(self.storage, self.counter, val[0], val[1])
        print('D: SENDING INITIAL: {} : {}'.format(val[0], frame))
        self.spooler.append_pending_ack(frame)
        self.spooler.append(frame)

