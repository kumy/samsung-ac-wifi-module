# -*- coding: utf-8 -*-
import sys
from binascii import hexlify

from osw.Frame import Frame
from osw.FrameBuilder import build_frame_ack

try:
    import asyncio
except:
    import uasyncio as asyncio


class FrameReceiver:
    raw = None
    len = None

    def __init__(self, storage, spooler, streamer=None):
        self.reset()
        self.spooler = spooler
        self.storage = storage
        self.streamer = streamer

    def set_streamer(self, streamer):
        if streamer is not None:
            self.streamer = streamer

    def reset(self):
        self.raw = bytearray()
        self.len = 0

    async def process(self, streamer=None):
        self.set_streamer(streamer)

        while True:
            char = await self.streamer.read()

            if char == b'' or char is None:
                await asyncio.sleep(1)
            elif not char:
                print('D: FrameReceiver.process: Client disconnected! - DEBUG 3')
                break

            self.append(char)

    def append(self, char):
        # print('D: FrameReceiver.process(): {}'.format(hexlify(char)))
        if char is None or char == b'':
            print('W: FrameReceiver.process: skip empty')
            return

        if len(self.raw) == 0 and char != b'\xd0':
            print('W: FrameReceiver.process: skip {}'.format(hexlify(char)))
            return
        self.raw.extend(char)
        frame_len = len(self.raw)

        if frame_len < 4:
            return
        elif frame_len == 4:
            self.len = self.raw[3]
            return
        elif frame_len - 4 < self.len:
            return

        self._process_frame()

    def _process_frame(self):
        print('D: FrameReceiver._process_frame(): {}'.format(hexlify(self.raw)))
        frame = Frame(self.raw)
        self.reset()
        self.storage.set_frame(frame)

        if frame.is_ack():
            self.spooler.receive_ack(frame)
        else:
            self.spooler.append(build_frame_ack(frame))


def test():
    print('Hello Test')


if __name__ == "__main__":
    # execute only if run as a script
    test()
