# -*- coding: utf-8 -*-

def int2bytes(counter, format=6):
    return counter.to_bytes(format, 'big')


def bytes2int(counter, format=6):
    return int.from_bytes(counter, 'big')


class FrameCounter:
    _counter = None

    def get_next(self):
        if self._counter is None:
            self._counter = 0
        else:
            self._counter += 1
        return int2bytes(self._counter)

    def save(self, counter):
        if self._counter is None:
            self._counter = bytes2int(bytes(counter))

        self._counter = max(self._counter, bytes2int(bytes(counter)))


def test():
    print('Hello Test')

    print(int2bytes(1) == bytes.fromhex('000000000001'))
    print(int2bytes(65535) == bytes.fromhex('00000000ffff'))
    print(bytes2int(b'\x00\x00\x00\x00\x00\x01') == 1)
    print(bytes2int(b'\x00\x00\x00\x00\xff\xff') == 65535)
    print(bytes2int(b'\xff\xff\xff\xff\xff\xff') == 281474976710655)

    counter = FrameCounter()
    print(counter.get_next() == b'\x00\x00\x00\x00\x00\x00')
    print(counter.get_next() == b'\x00\x00\x00\x00\x00\x01')
    counter.save(b'\x00\x00\x00\x00\x00\xff')
    print(counter._counter == 255)
    counter.save(b'\x00\x00\x00\x00\x00\x12')
    print(counter._counter == 255)


if __name__ == "__main__":
    # execute only if run as a script
    test()
