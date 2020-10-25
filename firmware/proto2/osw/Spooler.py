# -*- coding: utf-8 -*-
# from osw import spooler, counter, storage
from binascii import hexlify

from osw.FrameBuilder import build_frame_ack

try:
    import asyncio
except:
    import uasyncio as asyncio
import collections


# TODO resend un-ack-ed frames

class Spooler:
    _queue = collections.deque(tuple(), 10)
    _ack_queue = dict()

    def __init__(self, streamer, counter):
        self.streamer = streamer
        self.counter = counter

    def append(self, frame):
        self._queue.append(frame)

    def append_pending_ack(self, frame):
        self._ack_queue[frame.counter] = frame

    def receive_ack(self, frame):
        if frame.counter not in self._ack_queue.keys():
            print('W: unattended ack received with counter id: {}'.format(hexlify(frame.counter)))
            return
        del self._ack_queue[frame.counter]

    async def process(self):
        while True:
            if len(self._queue) == 0:
                await asyncio.sleep(1)
                continue

            frame = self._queue.popleft()
            print('D: Spooler.process()             : send     {}'.format(frame))
            if await self.streamer.write(frame.get()):
                self.counter.save(frame.counter)
            else:
                # requeue
                self.append(frame)
                # TODO sort spool by counter?
                print('W: Spooler.process(): Not connected, re-spool frame')

            await asyncio.sleep(1)

