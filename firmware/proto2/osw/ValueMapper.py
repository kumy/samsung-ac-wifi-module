# -*- coding: utf-8 -*-
from binascii import hexlify

MAPPER = {
    b'\x12': {
        b'\x01': {'name': 'AC_FUN_ENABLE', 'allowed': {b'\x0f': 'Enable', b'\xf0': 'Disable'}},
        b'\x02': {'name': 'AC_FUN_POWER', 'allowed': {b'\x0f': 'On', b'\xf0': 'Off'}},
        b'\x41': {'name': 'UNKNOWN_41', 'allowed': {}},
        b'\x43': {'name': 'AC_FUN_OPMODE',
                  'allowed': {b'\x12': 'Cool', b'\x22': 'Dry', b'\x32': 'Wind', b'\x42': 'Heat', b'\xe2': 'Auto'}},
        b'\x44': {'name': 'AC_FUN_COMODE',
                  'allowed': {b'\x12': 'Off', b'\x22': 'TurboMode', b'\x32': 'Smart', b'\x42': 'Sleep',
                              b'\x52': 'Quiet', b'\x62': 'SoftCool', b'\x82': 'WindMode1', b'\x92': 'WindMode2',
                              b'\xa2': 'WindMode3'}},
        b'\x5a': {'name': 'AC_FUN_TEMPSET', 'allowed': {}},
        b'\x5c': {'name': 'AC_FUN_TEMPNOW', 'allowed': {}},
        b'\x62': {'name': 'AC_FUN_WINDLEVEL',
                  'allowed': {b'\x00': 'Auto', b'\x12': 'Low', b'\x14': 'Mid', b'\x16': 'High', b'\x18': 'Turbo'}},
        b'\x63': {'name': 'AC_FUN_DIRECTION',
                  'allowed': {b'\x12': 'Off', b'\x21': 'Indirect', b'\x31': 'Direct', b'\x41': 'Center',
                              b'\x51': 'Wide', b'\x61': 'Left', b'\x71': 'Right', b'\x81': 'Long', b'\x92': 'SwingUD',
                              b'\xa2': 'SwingLR', b'\xb2': 'Rotation', b'\xc2': 'Fixed'}},
        b'\x73': {'name': 'AC_FUN_SLEEP', 'allowed': {}},
        b'\x74': {'name': 'UNKNOWN_41', 'allowed': {}},
        b'\xea': {'name': 'UNKNOWN_EA', 'allowed': {}},
        b'\xf7': {'name': 'AC_FUN_ERROR', 'allowed': {}, 'format': 'str'},
    },
    b'\x13': {
        b'\x32': {'name': 'AC_ADD_AUTOCLEAN', 'allowed': {b'\x22': 'On', b'\x23': 'Off'}},
        b'\x40': {'name': 'AC_ADD_SETKWH', 'allowed': {}},
        b'\x43': {'name': 'AC_ADD_STARTWPS', 'allowed': {b'\x0f': 'Default', b'\x20': 'Direct'}},  # TODO Other values??
        b'\x44': {'name': 'AC_ADD_CLEAR_FILTER_ALARM', 'allowed': {}},
        b'\x75': {'name': 'AC_ADD_SPI', 'allowed': {b'\x0f': 'On', b'\xf0': 'Off'}},
        b'\x76': {'name': 'AC_OUTDOOR_TEMP', 'allowed': {}},
        b'\x77': {'name': 'AC_COOL_CAPABILITY', 'allowed': {}},
        b'\x78': {'name': 'AC_WARM_CAPABILITY', 'allowed': {}},
        # b'\x??':    {'name': 'AC_ADD_APMODE_END', 'allowed': {}},
    },
    b'\x14': {
        b'\x17': {'name': 'UNKNOWN_17', 'allowed': {}},
        b'\x18': {'name': 'UNKNOWN_18', 'allowed': {}},
        b'\x19': {'name': 'UNKNOWN_19', 'allowed': {}},
        b'\x32': {'name': 'AC_ADD2_USEDWATT', 'allowed': {}},
        b'\x37': {'name': 'AC_SG_WIFI', 'allowed': {b'\x0f': 'Connected', b'\xf0': 'Disconnected'}},
        b'\x38': {'name': 'AC_SG_INTERNET', 'allowed': {b'\x0f': 'Connected', b'\xf0': 'Disconnected'}},
        b'\x39': {'name': 'AC_ADD2_OPTIONCODE', 'allowed': {}},
        b'\xe0': {'name': 'AC_ADD2_USEDPOWER', 'allowed': {}},
        b'\xe4': {'name': 'AC_ADD2_USEDTIME', 'allowed': {}},
        b'\xe6': {'name': 'AC_ADD2_FILTER_USE_TIME', 'allowed': {}},
        b'\xe8': {'name': 'AC_ADD2_CLEAR_POWERTIME', 'allowed': {}},
        b'\xe9': {'name': 'AC_ADD2_FILTERTIME', 'allowed': {b'\x01': '0', b'\x02': '300', b'\x03': '500', b'\x04': '700'}},
        b'\xf3': {'name': 'AC_ADD2_OUT_VERSION', 'allowed': {}},
        b'\xf4': {'name': 'AC_ADD2_PANEL_VERSION', 'allowed': {}},
        b'\xf5': {'name': 'AC_FUN_MODEL', 'allowed': {}},
        b'\xf6': {'name': 'AC_ADD2_VERSION', 'allowed': {}},
        b'\xf7': {'name': 'AC_SG_MACHIGH', 'allowed': {}},
        b'\xf8': {'name': 'AC_SG_MACMID', 'allowed': {}},
        b'\xf9': {'name': 'AC_SG_MACLOW', 'allowed': {}},
        b'\xfa': {'name': 'AC_SG_VENDER01', 'allowed': {}},
        b'\xfb': {'name': 'AC_SG_VENDER02', 'allowed': {}},
        b'\xfc': {'name': 'AC_SG_VENDER03', 'allowed': {}},
        b'\xfd': {'name': 'UNKNOWN_FD', 'allowed': {}},
    },
}


def get_register_details(command, register):
    if command in MAPPER.keys() and register in MAPPER[command].keys():
        return MAPPER[command][register]

    return {'name': 'UNKNOWN_{:0>2x}'.format(int.from_bytes(register, "big")), 'allowed': {}}


def get_value_mapping(command, register, value):
    allowed = get_register_details(command, register)['allowed']

    if value and allowed and value in allowed.keys():
        return allowed[value]
    return int.from_bytes(value, 'big') if value else None
    # return hexlify(value).decode('ascii')