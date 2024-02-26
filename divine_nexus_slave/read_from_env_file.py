import uio

def read_env_file(filename):
    env = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()
    except OSError:
        print("Error: Unable to read .env file")
    return env

# Usage example:
env = read_env_file(".env")
print("Environment variables:", env)


# wifi_ssid = env.get("WIFI_SSID")
# wifi_password = env.get("WIFI_PASSWORD")

# print("Wi-Fi SSID:", wifi_ssid)
# print("Wi-Fi Password:", wifi_password)
