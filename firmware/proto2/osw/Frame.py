# -*- coding: utf-8 -*-
from binascii import hexlify

from osw.Storage import x_to_bytes, x_to_bytearray


def compute_checksum(data):
    chk = 0
    for el in data:
        chk ^= el
    return chk


class Frame:
    raw = None
    counter = None
    command = None
    ack = None
    values = None

    def __init__(self, raw):
        self.set(raw)

    def get(self):
        return self.raw

    def set(self, value):
        self.values = list()
        self.counter = None
        self.command = None
        self.ack = None

        self.raw = x_to_bytearray(value)
        self._decode()

    def is_ack(self):
        return self.raw[12] % 2 == 1

    def __str__(self):
        return hexlify(self.raw).decode("ascii")

    def _decode(self):
        checksum = compute_checksum(self.raw[:-2])
        if self.raw[-2] != checksum:
            print('W: Frame: Invalid checksum {} should be {}'.format(
                hexlify(x_to_bytes(self.raw[-2])).decode("ascii"),
                hexlify(bytes([checksum])).decode("ascii")),
            )
            return

        self.counter = self.raw[4:10]
        self.command = self.raw[12]
        self.ack = self.raw[12]

        frame_length = self.raw[3] + 2
        idx = 14
        while True:
            register = x_to_bytes(self.raw[idx])
            length = self.raw[1 + idx]
            value = x_to_bytes(self.raw[2 + idx:2 + idx + length])
            idx += 2 + length
            if length == 0:
                idx += 1
            # print("W: Frame:  idx:{} len:{}".format(idx, length))

            self.values.append((register, value))
            if idx == frame_length:
                break

            if idx > frame_length:
                print("W: Frame: Wrong payload/length: {} > {}".format(idx, frame_length))
                break


def test():
    print('Hello Test')
    print('TEST 1:')
    raw = 'd0c00212000000000000fe12040601010f7401f064e0'
    frame = Frame(raw)
    print(frame)

    print('TEST 2:')
    frame.set(raw)
    print(frame)

    print('TEST 3:')
    raw = b'\xd0\xc0\x02\x12\x00\x00\x00\x00\x00\x00\xfe\x12\x04\x06\x01\x01\x0f\x74\x01\xf0\x64\xe0'
    frame.set(raw)
    print(frame)

    print('TEST 4:')
    raw = bytearray(b'\xd0\xc0\x02\x12\x00\x00\x00\x00\x00\x00\xfe\x12\x04\x06\x01\x01\x0f\x74\x01\xf0\x64\xe0')
    frame.set(raw)
    print(frame)


if __name__ == "__main__":
    # execute only if run as a script
    test()