import network
import urequests as requests
import utime
import ubinascii

# WiFi Credentials
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Camera URL and authentication
CAMERA_URL = "http://192.168.2.111/ISAPI/Streaming/channels/402/picture"
AUTH_USERNAME = "view"
AUTH_PASSWORD = "VIEWview"

# Pushover API details
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_TOKEN = "ave1e35sczs3qd6d3dyi82hgprzouh"
PUSHOVER_USER = "ut57cr2s6bbro616zngdr6soaheaac"

# File path for saving image
IMAGE_PATH = "image.jpg"

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        utime.sleep(1)
    print("Connected:", wlan.ifconfig())

# Fetch JPEG Image
def fetch_image(url, filename):
    """Fetch an image from the camera and save it as a file."""
    headers = {
        "Authorization": "Basic " + ubinascii.b2a_base64(AUTH_USERNAME + ":" + AUTH_PASSWORD).decode().strip()
    }

    print("Fetching image...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to fetch image: {response.status_code}")

    response.close()

# Encode Image as Base64
def encode_image_base64(filename):
    """Read an image and encode it as Base64 for sending to Pushover."""
    print("Encoding image as Base64...")
    with open(filename, "rb") as img_file:
        img_base64 = ubinascii.b2a_base64(img_file.read()).decode().strip()
    return img_base64

# Send Image as Base64 to Pushover
def send_image(image_base64):
    """Send Base64-encoded image as a Pushover notification."""
    print("Sending Pushover notification with image...")
    
    data = {
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": "CCTV Alert: Motion detected",
        "attachment": image_base64,  # Attach the Base64-encoded image
        "attachment_type": "image/jpeg",
        "attachment_name": "image.jpg"
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(PUSHOVER_URL, json=data, headers=headers)

    print("Pushover Response:", response.text)

# Main Execution
# connect_wifi()
fetch_image(CAMERA_URL, IMAGE_PATH)
image_base64 = encode_image_base64(IMAGE_PATH)
send_image(image_base64)
