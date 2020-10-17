
from machine import Pin
import uasyncio as asyncio
import socket
from ubinascii import hexlify

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
        self.group = data[:2]
        self.ack = data[2]
        self.command = data[3:4]
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
        self.cmd = CMD(self.command, self.payload)


class CMD:
    GROUP = None
    CMD = None

    command = None
    payload = None

    values = None

    # TODO, registers 43 and 44 apear multiple time
    REGISTERS = {
        b'\x01':    {'name': 'AC_FUN_ENABLE', 'allowed': {b'\x0f': 'Enable', b'\xf0': 'Disable'}},
        b'\x02':    {'name': 'AC_FUN_POWER', 'allowed': {b'\x0f': 'Enable', b'\xf0': 'Disable'}},
        b'\x41':    {'name': 'UNKNOWN_41', 'allowed': {}},
        b'\x43':    {'name': 'AC_FUN_OPMODE', 'allowed': {b'\x12': 'Cool', b'\x22': 'Dry', b'\x32': 'Wind', b'\x42': 'Heat', b'\xe2': 'Auto'}},
        b'\x44':    {'name': 'AC_FUN_COMODE', 'allowed': {b'\x12': 'Off', b'\x22': 'TurboMode', b'\x32': 'Smart', b'\x42': 'Sleep', b'\x52': 'Quiet', b'\x62': 'SoftCool', b'\x82': 'WindMode1', b'\x92': 'WindMode2', b'\xa2': 'WindMode3'}},
        b'\x5a':    {'name': 'AC_FUN_TEMPSET', 'allowed': {}},
        b'\x5c':    {'name': 'AC_FUN_TEMPNOW', 'allowed': {}},
        b'\x62':    {'name': 'AC_FUN_WINDLEVEL', 'allowed': {b'\x00': 'Auto', b'\x12': 'Low', b'\x14': 'Mid', b'\x16': 'High', b'\x18': 'Turbo'}},
        b'\x63':    {'name': 'AC_FUN_DIRECTION', 'allowed': {b'\x12': 'Off', b'\x21': 'Indirect', b'\x31': 'Direct', b'\x41': 'Center', b'\x51': 'Wide', b'\x61': 'Left', b'\x71': 'Right', b'\x81': 'Long', b'\x92': 'SwingUD', b'\xa2': 'SwingLR', b'\xb2': 'Rotation', b'\xc2': 'Fixed'}},
        b'\x73':    {'name': 'AC_FUN_SLEEP', 'allowed': {}},
        b'\xea':    {'name': 'UNKNOWN_EA', 'allowed': {}},
        b'\xf7':    {'name': 'AC_FUN_ERROR', 'allowed': {}},
    }


    REGISTERS2 = {
        b'\x32':    {'name': 'AC_ADD_AUTOCLEAN', 'allowed': {b'\x22': 'On', b'\x23': 'Off'}},
        b'\x37':    {'name': 'AC_SG_WIFI', 'allowed': {b'\x0f': 'Connected', b'\xf0': 'Disconnected'}},
        b'\x38':    {'name': 'AC_SG_INTERNET', 'allowed': {b'\x0f': 'Connected', b'\xf0': 'Disconnected'}},
        b'\x39':    {'name': 'AC_ADD2_OPTIONCODE', 'allowed': {}},
        b'\x40':    {'name': 'AC_ADD_SETKWH', 'allowed': {}},
        b'\x42':    {'name': 'AC_ADD2_USEDWATT', 'allowed': {}},
        b'\x43':    {'name': 'AC_ADD_STARTWPS', 'allowed': {}},
        b'\x44':    {'name': 'AC_ADD_CLEAR_FILTER_ALARM', 'allowed': {}},
        b'\x75':    {'name': 'AC_ADD_SPI', 'allowed': {}},
        b'\x76':    {'name': 'AC_OUTDOOR_TEMP', 'allowed': {}},
        b'\x77':    {'name': 'AC_COOL_CAPABILITY', 'allowed': {}},
        b'\x78':    {'name': 'AC_WARM_CAPABILITY', 'allowed': {}},
        b'\xe0':    {'name': 'AC_ADD2_USEDPOWER', 'allowed': {}},
        b'\xe4':    {'name': 'AC_ADD2_USEDTIME', 'allowed': {}},
        b'\xe6':    {'name': 'AC_ADD2_FILTER_USE_TIME', 'allowed': {}},
        b'\xe8':    {'name': 'AC_ADD2_CLEAR_POWERTIME', 'allowed': {}},
        b'\xe9':    {'name': 'AC_ADD2_FILTERTIME', 'allowed': {}},
        b'\xf3':    {'name': 'AC_ADD2_OUT_VERSION', 'allowed': {}},
        b'\xf4':    {'name': 'AC_ADD2_PANEL_VERSION', 'allowed': {}},
        b'\xf5':    {'name': 'AC_FUN_MODEL', 'allowed': {}},
        b'\xf6':    {'name': 'AC_ADD2_VERSION', 'allowed': {}},
        b'\xf7':    {'name': 'AC_SG_MACHIGH', 'allowed': {}},
        b'\xf8':    {'name': 'AC_SG_MACMID', 'allowed': {}},
        b'\xf9':    {'name': 'AC_SG_MACLOW', 'allowed': {}},
        b'\xfa':    {'name': 'AC_SG_VENDER01', 'allowed': {}},
        b'\xfb':    {'name': 'AC_SG_VENDER02', 'allowed': {}},
        b'\xfc':    {'name': 'AC_SG_VENDER03', 'allowed': {}},
    }

    def get_register_details(self, register):
        if register in self.REGISTERS.keys():
            return self.REGISTERS[register]
        if register in self.REGISTERS2.keys():
            return self.REGISTERS2[register]

        return {'name': 'UNKNOWN_{:0>2x}'.format(int.from_bytes(register, "big")), 'allowed': {}}

    def get_value_mapping(self, register, value):
        allowed = None
        if register in self.REGISTERS.keys():
            allowed = self.REGISTERS[register]['allowed']
        if register in self.REGISTERS2.keys():
            allowed = self.REGISTERS2[register]['allowed']

        if value and allowed and value in allowed.keys():
            return allowed[value]
        return value

    def __init__(self, command, payload):
        self.command = command
        self.payload = payload

        self.values = []
        idx = 0
        while True:
            register = bytes([payload[0 + idx]])
            length = payload[1 + idx]
            value = bytes(payload[2 + idx:2 + length + idx])
            t = (
                register,
                length,
                int.from_bytes(value, "big"),
                self.get_register_details(register)['name'],
                self.get_value_mapping(register, value),
            )
            idx += 2 + length
            self.values.append(t)

            if idx == len(self.payload):
                break

            if idx >= len(self.payload):
                print("Should not happen")
                break

    def print(self):
        for val in self.values:
            write(val[0])
            write(val[1])
            write(val[2])
            write('.')

    def print_txt(self):
        for val in self.values:
            if isinstance(val[4], bytes):
                print('{}:{} '.format(val[3], int.from_bytes(val[4], "big")), end='')
            else:
                print('{}:{} '.format(val[3], val[4]), end='')


async def receiver():
    ureader = asyncio.StreamReader(s)
    frame = Frame()
    while True:
        res = await ureader.read(1)
        if res is not None:
            # pass
            # print(hexlify(res))
            frame.append(res)


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
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')

print('END.')
