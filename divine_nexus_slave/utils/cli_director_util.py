from command_lines_proc import (
    led, board_temperature
)


def cli_director(cli):
    if cli == "led_on":
        led.on()
        return True, "LED Turned On"
    elif cli == "led_off":
        led.off()
        return True, "LED Turned Off"
    elif cli == "board_temperature":
        temp = board_temperature()
        return True, temp
    
