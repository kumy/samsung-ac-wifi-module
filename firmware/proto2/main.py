# -*- coding: utf-8 -*-


# from machine import UART
# import uos
# import socket
# from ubinascii import hexlify
#
#
# s = socket.socket()
# s.connect(('192.168.125.64', 8888))
# s.send(b'Hello\n')
#
# uos.dupterm(None, 1)
# uart = UART(0, baudrate=9600)
# uart.init(rxbuf=100)
# print('HELLO')
#
#
# def receiver(uart, soc):
#     while True:
#         res = uart.read(1)
#         if res:
#             print(hexlify(res))
#             soc.send(res)
#
#
# def mainUart(uart, swriter):
#     receiver(uart, swriter)
#
#
# try:
#     mainUart(uart, s)
# except KeyboardInterrupt:
#     print('Interrupted')
# finally:
#     uart = UART(0, 115200)
#     uos.dupterm(uart, 1)

#########################################

# import uos
# from machine import UART, Pin
#
# try:
#     import asyncio
# except:
#     import uasyncio as asyncio
#
# HOST='192.168.125.64'
# PORT=8888
#
#
# async def blink(led, period_ms):
#     while True:
#         led.off()
#         await asyncio.sleep_ms(5)
#         led.on()
#         await asyncio.sleep_ms(period_ms)
#
#
# async def uart_reader(ureader, swriter):
#     while True:
#         char = await ureader.read(1)
#         print('uart_reader:', char)
#         swriter.write(char)
#         await swriter.drain()
#
#
# async def socket_reader(sreader, uwriter):
#     while True:
#         char = await sreader.read(1)
#         print('socket_reader:', char)
#         uwriter.write(char)
#         await uwriter.drain()
#
#
# async def main():
#     sreader, swriter = await asyncio.open_connection(HOST, PORT)
#     swriter.write(b' HELLO !!!')
#     await swriter.drain()
#     uart = UART(0, baudrate=9600)
#     uart.init(rxbuf=100)
#     uos.dupterm(None, 1)
#     ureader = asyncio.StreamReader(uart)
#     swriter.write(b' HELLO 2 !!!')
#
#     asyncio.create_task(blink(Pin(16, Pin.OUT), 700))
#     asyncio.create_task(blink(Pin(2, Pin.OUT), 400))
#     asyncio.create_task(uart_reader(ureader, swriter))
#     asyncio.create_task(socket_reader(sreader, ureader))
#     while True:
#         await asyncio.sleep(1)
#
# try:
#     asyncio.run(main())
# except KeyboardInterrupt:
#     print('Interrupted')
# finally:
#     uart = UART(0, 115200)
#     uos.dupterm(uart, 1)
#
# print('END.')

####################

from machine import UART
import uos
import uasyncio as asyncio
from ubinascii import hexlify


uart = UART(0, baudrate=9600)
uart.init(rxbuf=100)
uos.dupterm(None, 1)


async def uart_reader(ureader, swriter):
    swriter.write('U')
    await swriter.drain()
    while True:
        res = await ureader.read(100)
        if res is not None:
            print('uart_reader:', hexlify(res))
            swriter.write(res)
            await swriter.drain()


async def socket_reader(sreader, uwriter):
    sreader.write('S')
    await sreader.drain()
    while True:
        res = await sreader.read(100)
        print('socket_reader:', hexlify(res))
        uwriter.write(res)
        await uwriter.drain()


async def main():
    ureader = asyncio.StreamReader(uart)
    sreader, swriter = await asyncio.open_connection('192.168.125.64', 8888)

    asyncio.create_task(uart_reader(ureader, swriter))
    await asyncio.sleep(1)
    asyncio.create_task(socket_reader(sreader, ureader))

    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    uart = UART(0, 115200)
    uos.dupterm(uart, 1)
    print('END')

print('END.')

