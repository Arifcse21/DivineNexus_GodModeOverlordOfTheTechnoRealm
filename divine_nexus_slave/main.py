import network
import usocket as socket
import ujson
import ubinascii
import os


# Define your Wi-Fi credentials
wifi_ssid = "OpenWifi"
wifi_password = "#IndiaOut,Fuck USA!!"

# Function to connect to Wi-Fi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(wifi_ssid, wifi_password)
    while not wifi.isconnected():
        pass
    print("Connected to Wi-Fi")

# Define WebSocket server details
websocket_server = "192.168.0.4"  # Assuming the WebSocket server is running locally
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

# Main function to handle WebSocket communication
def main():
    connect_wifi()
    while True:
        websocket = connect_websocket()
        if websocket:
            # Send a message (optional)
            message = {"message": "Hello from ESP32!"}
            websocket.send(ujson.dumps(message))

            # Main loop
            while True:
                try:
                    data = websocket.recv(1024)
                    if data:
                        print("Received message:", data)
                except OSError as e:
                    print("WebSocket connection error:", e)
                    break

# Run the main function
main()
