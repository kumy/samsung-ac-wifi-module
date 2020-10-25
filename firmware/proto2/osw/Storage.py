# -*- coding: utf-8 -*-
from binascii import hexlify


def x_to_bytearray(value):
    return x_to_bytes(value)


def x_to_bytes(value):
    if isinstance(value, str):
        return bytes.fromhex(value)
    if isinstance(value, int):
        return bytes([value])
    if isinstance(value, bytearray):
        return bytes(value)
    return value


class Storage:
    storage = dict()  # same storage for any instance

    def __init__(self):
        self.storage = {
            b'\x12': {
                b'\x01': b'\x0f',
                b'\x02': b'\x00',
                b'\x41': b'\x00',
                b'\x43': b'\x00',
                b'\x44': b'\x00',
                b'\x5a': b'\x00',
                b'\x5c': b'\x00',
                b'\x62': b'\x00',
                b'\x63': b'\x00',
                b'\x73': b'\x00',
                b'\x74': b'\xf0',
                b'\xea': b'\x00',
                b'\xf7': b'\x00',
            },
            b'\x13': {
                b'\x32': b'\x00',
                b'\x40': b'\x00',
                b'\x43': b'\x00',
                b'\x44': b'\x00',
                b'\x75': b'\x00',
                b'\x76': b'\x00',
                b'\x77': b'\x00',
                b'\x78': b'\x00',
            },
            b'\x14': {
                b'\x17': b'\x15',
                b'\x18': b'\x05',
                b'\x19': b'\x27',
                b'\x32': b'\x00',
                b'\x37': b'\x0f',
                b'\x38': b'\xf0',
                b'\x39': b'\x00',
                b'\xe0': b'\x00',
                b'\xe4': b'\x00',
                b'\xe6': b'\x00',
                b'\xe8': b'\x00',
                b'\xe9': b'\x00',
                b'\xf3': b'\x00',
                b'\xf4': b'\x00',
                b'\xf5': b'\x00',
                b'\xf6': b'\x00',
                b'\xfd': b'\x02',

                # Mac address
                b'\xfa': b'\x00',
                b'\xfb': b'\x00',
                b'\xfc': b'\x00',
                b'\xf7': b'\x00',
                b'\xf8': b'\x00',
                b'\xf9': b'\x00',
            },
        }

    def get(self, command, register):
        cmd = x_to_bytes(command)[:1]
        reg = x_to_bytes(register)[:1]

        if cmd in self.storage and reg in self.storage[cmd]:
            return self.storage[cmd][reg]
        print('W: requested unknown register: {}.{}'.format(hexlify(cmd), hexlify(reg)))
        return None

    def set(self, command, register, value):
        cmd = x_to_bytes(command)[:1]
        reg = x_to_bytes(register)[:1]

        if cmd not in self.storage:
            self.storage[cmd] = {}
        self.storage[cmd][reg] = value

    def set_frame(self, frame):
        for val in frame.values:
            self.set(frame.command, val[0], val[1])


def test():
    print('Hello Test')

    print('TEST 1:')

    print('TEST 2:')
    storage = Storage()
    print(storage.get(b'\x14', b'\xfa'),
          storage.get(b'\x14', b'\xfb'),
          storage.get(b'\x14', b'\xfc'),
          storage.get(b'\x14', b'\xf7'),
          storage.get(b'\x14', b'\xf8'),
          storage.get(b'\x14', b'\xf9'),
          )

    print('TEST 3:')
    storage.set(b'\x14', b'\xfa', b'\x12')
    print(storage.get(b'\x14', b'\xfa') == b'\x12')

    print('TEST 4:')
    storage.set(20, b'\xfa', b'\x12')
    print(storage.get(b'\x14', b'\xfa') == b'\x12')


if __name__ == "__main__":
    # execute only if run as a script
    test()
