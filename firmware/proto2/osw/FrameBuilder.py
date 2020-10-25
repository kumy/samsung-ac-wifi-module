# -*- coding: utf-8 -*-
from osw.Frame import compute_checksum, Frame
from osw.Storage import x_to_bytes


def build_frame(storage, counter, command, values):
    if command is None or len(values) == 0:
        raise Exception('Missing required values to build a frame')
    # TODO check command

    payload = bytearray()

    if x_to_bytes(command)[1] == 2:  # request mode
        for value in values:
            payload += x_to_bytes(value)
            payload += b'\0'
    else:
        for value in values:
            val = storage.get(command, value)
            payload += x_to_bytes(value)
            if val is None:
                payload += b'\0'
            else:
                payload += bytes([len(val)])
                payload += val
            # payload += b'\0' if val == b'\0' else bytes([len(val)])
            # payload += val

    frame = bytearray()
    frame.extend(b'\xd0\xc0\x02')
    frame.append(12+len(payload))
    frame.extend(counter if isinstance(counter, bytes) else counter.get_next())
    frame.extend(b'\xfe')
    frame.extend(command)
    frame.append(len(payload))
    frame.extend(payload)
    frame.append(compute_checksum(frame))
    frame.extend(b'\xe0')

    frm = Frame(frame)
    return Frame(frame)


def build_frame_ack(frame, storage=None):
    def simple():
        response = bytearray()
        response[:] = frame.get() if isinstance(frame, Frame) else frame
        response[12] += 1
        response[-2] = compute_checksum(response[:-2])

        resp = Frame(response)
        return resp

    def request():
        values = [x[0] for x in frame.values]
        resp = build_frame(storage, frame.counter, frame.command + bytes([frame.ack[0] + 1]), values)
        return resp

    if frame.is_request():
        return request()
    return simple()


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
