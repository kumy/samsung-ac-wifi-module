# -*- coding: utf-8 -*-
from binascii import hexlify

from aiohttp import web

from osw.ValueMapper import get_register_details, get_value_mapping


def start_web(storage):
    async def handler_index(request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def handler_values(request):
        data = {
            hexlify(k).decode('ascii'): {
                # hexlify(k2).decode('ascii'): hexlify(v2).decode('ascii') for k2, v2 in v.items()
                get_register_details(k, k2)['name']: get_value_mapping(k, k2, v2) for k2, v2 in v.items()
            } for k, v in storage.storage.items()
        }
        return web.json_response(data)

    app = web.Application()
    app.add_routes([
        web.get('/', handler_index),
        web.get('/values', handler_values),
        web.get('/{name}', handler_index),
    ])
    return app
