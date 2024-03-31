command_tuples = (
    ('led_on', 'led_on'),
    ('led_off', 'led_off'),
    ('board_temperature', 'board_temperature'),
    ('command4', 'command4'),
    ('command5', 'command5'),
    ('command6', 'command6'),
    ('command7', 'command7'),
    ('command8', 'command8'),
    ('command9', 'command9'),
    ('command10', 'command10'),
    ('command11', 'command11'),
    ('command12', 'command12'),
)

topics_to_pub_dict = {
    'led_on': 'esp32/led_on',
    'led_off': 'esp32/led_off',
    'board_temperature': 'esp32/board_temperature',
    'command4': 'esp32/command4',
    'command5': 'esp32/command5',
    'command6': 'esp32/command6',
    'command7': 'esp32/command7',
    'command8': 'esp32/command8',
    'command9': 'esp32/command9',
    'command10': 'esp32/command10',
    'command11': 'esp32/command11',
    'command12': 'esp32/command12',
}

topics_to_sub_list = [
    "rpi/led_on",
    "rpi/led_off",
    "rpi/board_temperature",
    "rpi/command4",
    "rpi/command5",
    "rpi/command6",
    "rpi/command7",
    "rpi/command8",
    "rpi/command9",
    "rpi/command10",
    "rpi/command11",
    "rpi/command12",
]