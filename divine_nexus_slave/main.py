import network
import usocket as socket
import ujson
import ubinascii
import os
import time
from cli_director import cli_director


# Define your Wi-Fi credentials
wifi_ssid = "IndiaOut"
wifi_password = "FuckUSA"

# Function to connect to Wi-Fi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(wifi_ssid, wifi_password)
    while not wifi.isconnected():
        pass
    print("Connected to Wi-Fi")

# Define WebSocket server details
websocket_server = "192.168.68.107"  # Assuming the WebSocket server is running locally
websocket_port = 8000
websocket_path = "/ws/command/"

# Function to generate a suitable Sec-WebSocket-Key
def generate_websocket_key():
    key = os.urandom(16)
    return ubinascii.b2a_base64(key).decode().strip()

# Function to establish WebSocket connection
def connect_websocket():
    # Create a socket
    s = socket.socket()

    # Resolve the WebSocket server address
    addr = socket.getaddrinfo(websocket_server, websocket_port)[0][-1]

    # Connect to the server
    s.connect(addr)

    # Generate the WebSocket key
    websocket_key = generate_websocket_key()

    # Construct the WebSocket handshake
    handshake = "GET {} HTTP/1.1\r\n".format(websocket_path)
    handshake += "Host: {}\r\n".format(websocket_server)
    handshake += "Connection: Upgrade\r\n"
    handshake += "Upgrade: websocket\r\n"
    handshake += "Sec-WebSocket-Key: {}\r\n".format(websocket_key)
    handshake += "Sec-WebSocket-Version: 13\r\n\r\n"

    # Send the handshake
    s.send(handshake)

    # Read the response
    response = s.recv(1024)
    print(response)
    # Check if the handshake was successful
    if response.decode().find(" 101 ") != -1:
        print("WebSocket connection established")
        return s
    else:
        print("Failed to establish WebSocket connection")
        return None
    
def process_message(message):
    # Check if the message starts with the text frame indicator (0x81)
    if message.startswith(b'\x81'):
        # Decode the message and process it as a JSON payload
        try:
            decoded_message = message[4:].decode()
            parsed_message = ujson.loads(decoded_message)
            # Process the JSON message
            # print("Received JSON message:", parsed_message)
            return parsed_message
        except:
            # print("Received non-JSON message:", message)
            return {}
    else:
        # print("Received non-text message:", message)
        return {}



# Main function to handle WebSocket communication
def main():
    connect_wifi()
    while True:
        websocket = connect_websocket()
        counter = 0
        while True:
            counter += 1
            try:
                data = websocket.recv(4096)
                if data:
                    command_value = None
                    processed_data = process_message(data)
                    if processed_data:
                        command_value = processed_data["data"]["command"]
                        stat, msg = cli_director(command_value)
                        if stat:
                            resp_data = {
                                "type": "execution",
                                "data": msg
                            }
                            resp_data_json = ujson.dumps(resp_data)	#.encode("utf-8")
                            
                            try:
                                print(type(resp_data_json))
                                websocket.send(resp_data_json)
                                print("JSON data sent successfully:", resp_data_json)
                            except Exception as e:
                                print("here error", type(e).__name__)
                                
                    print(f"{command_value if command_value else ''}")
            except OSError as e:
                print(f"WebSocket connection error {counter}:", e)
                break  # Exit the inner loop to attempt reconnection
        # Attempt reconnection after encountering an error
        time.sleep(1)  # Add a delay before attempting reconnection

# Run the main function
main()

