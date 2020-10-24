
from machine import Pin
import uasyncio as asyncio
import socket
from ubinascii import hexlify
import picoweb
# import ulogging as logging
import micropython
import gc
from samsungac import Command, CommandLookup

s = socket.socket()
s.connect(('192.168.125.64', 50007))


def write(data):
    if isinstance(data, bytearray):
        for x in data:
            print("{:0>2x}".format(x), end='')
    elif isinstance(data, bytes):
        write(bytearray(data))
    elif isinstance(data, int):
        print("{:0>2x}".format(data), end='')
    else:
        print(str(data), end='')


class Frame:
    START = bytearray(b'\xd0\xc0')
    VERSION = bytearray(b'\x02')
    END = bytearray(b'\xe0')

    def __init__(self):
        self.init()
        return None

    def init(self):
        self.frame = bytearray()

        self.start = None
        self.version = None
        self.len = None
        self.counter = None
        self.payload = None
        self.checksum = None
        self.end = None

        self.checksum_computed = None
        self.checksum_valid = None
        gc.collect()
        micropython.mem_info()

    def append(self, data):
        if len(self.frame) == 0 and data != b'\xd0':
            print(hexlify(data))
            return  # Skip data
        self.frame += bytearray(data)
        self._decode()

    def is_complete(self):
        return self.end is not None

    def _decode(self):
        if self.start is None:
            if self.frame == self.START:
                self.start = self.START
            return

        if self.version is None:
            self.version = self.frame[-1]
            return

        if self.len is None:
            self.len = self.frame[-1]
            return

        if self.counter is None:
            if len(self.frame) == 10:
                self.counter = self.frame[4:]
            return

        payload_len = self.len + 4
        if len(self.frame) < payload_len:
            return

        self.end = self.frame[-1]
        self.checksum = self.frame[-2]
        self.payload = Payload(self.frame[10:-2])
        # self.payload = self.frame[10:-2]

        self.checksum_computed = self.compute_checksum(self.frame[:-2])
        self.checksum_valid = (self.checksum_computed == self.checksum)

        self.print()
        self.init()

    def compute_checksum(self, data):
        chk = 0
        for el in data:
            chk ^= el
        return chk

    def print(self):
        write(self.start)
        write(" ")
        write(self.version)
        write(" ")
        write(self.len)
        write(" ")
        write(self.counter)
        write(" ")
        self.payload.print()
        write(" ")
        write(self.checksum)
        write(" ")
        write(self.end)
        if not self.checksum_valid:
            write(" !!! checksum error should be: {:0>2x}".format(self.checksum_computed))
        print()


class Payload:
    data = None

    group = None
    ack = None
    command = None
    payload = None

    cmd = None

    def __init__(self, data):
        self.data = data
        self.group = bytes([data[1]])
        self.ack = bytes([data[2]])
        self.command = bytes(data[3:4])
        self.payload = data[4:]
        self._decode()

    def __len__(self):
        return len(self.data)

    def print(self):
        write(self.group)
        write(' ')
        write(self.ack)
        write(' ')
        write(self.command)
        write(' ')
        if self.cmd:
            self.cmd.print()
        else:
            write(self.payload)

    def get_ack(self):
        ack = Payload(self.data)
        ack.data[2] += 1
        return ack

    def _decode(self):
        self.cmd = Command(lookup, storage, self.group, self.payload)


class Storage:
    def __init__(self):
        self.storage = {}

    def set(self, command, register, value):
        if command not in self.storage:
            self.storage[command] = {}
        self.storage[command][register] = value

    def get(self, command, register):
        return self.storage[command][register]


async def receiver():
    ureader = asyncio.StreamReader(s)
    frame = Frame()
    while True:
        res = await ureader.read(1)
        if res is not None:
            # pass
            # print(hexlify(res))
            frame.append(res)


def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req, storage, lookup))


ROUTES = [
    ("/", index),
    ("/css/chota.min.css", lambda req, resp: (yield from app.sendfile(resp, "css/chota.min.css"))),
]
# logging.basicConfig(level=logging.INFO)
app = picoweb.WebApp(__name__, ROUTES)


async def blink(led, period_ms):
    while True:
        led.off()
        await asyncio.sleep_ms(5)
        led.on()
        await asyncio.sleep_ms(period_ms)


async def main():
    asyncio.create_task(blink(Pin(16, Pin.OUT), 700))
    asyncio.create_task(blink(Pin(2, Pin.OUT), 400))
    asyncio.create_task(receiver())
    # while True:
    #     await asyncio.sleep(1)
    print('Starting webserver')
    app.run(debug=1, host='0.0.0.0')

try:
    storage = Storage()
    lookup = CommandLookup()
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    s.close()

print('END.')
