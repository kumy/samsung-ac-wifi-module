# -*- coding: utf-8 -*-
from osw.Frame import compute_checksum, Frame


def build_frame(spooler, storage, counter, command, values):
    if command is None or len(values) == 0:
        raise Exception('Missing required values to build a frame')
    # TODO check command

    payload = bytearray()
    for value in values:
        val = storage.get(command, value)
        payload += value
        payload += b'\0' if val == b'\0' else bytes([len(val)])
        payload += val

    frame = bytearray()
    frame.extend(b'\xd0\xc0\x02')
    frame.append(12+len(payload))
    frame.extend(counter.get_next())
    frame.extend(b'\xfe')
    frame.extend(command)
    frame.append(len(payload))
    frame.extend(payload)
    frame.append(compute_checksum(frame))
    frame.extend(b'\xe0')

    frm = Frame(frame)
    spooler.append_pending_ack(frm)
    spooler.append(frm)
    # return Frame(frame)


def build_frame_ack(frame):
    response = bytearray()
    response[:] = frame.get() if isinstance(frame, Frame) else frame
    response[12] += 1
    response[-2] = compute_checksum(response[:-2])

    resp = Frame(response)
    return resp


def test():
    print('Hello Test')

    print('TEST 1:')
    raw = 'd0c00212000000000000fe12040601010f7401f064e0'
    frame = Frame(raw)

    resp = build_frame_ack(frame)
    print(str(resp) == 'd0c00212000000000000fe12050601010f7401f065e0')

    print('TEST 2:')
    frame = build_frame(b'\x12\x04', [b'\x01', b'\x74'])
    print(str(frame) == raw)


if __name__ == "__main__":
    # execute only if run as a script
    test()
