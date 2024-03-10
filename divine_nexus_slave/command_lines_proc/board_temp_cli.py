import esp32

def board_temperature():
    tf = esp32.raw_temperature()
    tc = (tf-32.0)/1.8
    temperature = f"Temperature: {tf} deg F or {tc:.1f} deg C"

    return temperature
    

