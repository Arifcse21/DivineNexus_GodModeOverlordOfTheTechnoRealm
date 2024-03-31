from led_cli import led
from board_temp_cli import board_temperature


def cli_master(cli):
    if cli == "led_on":
        led.on()
        return True, "LED Turned On"
    elif cli == "led_off":
        led.off()
        return True, "LED Turned Off"
    elif cli == "board_temperature":
        temp = board_temperature()
        return True, temp
    
    
    else:
        return False, "Invalid Cli"
    

