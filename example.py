from printwatch.client import PrintWatchClient
from printwatch.utils import *
from time import sleep

# Insert API key
printer_info = init_default("")

# Create Client object
client = PrintWatchClient()

# Open an image to inference
with open('img.jpg', 'rb') as f:
  image = bytearray(f.read())

# Create the payload information
payload = client._create_payload(
    encoded_image = image,
    printer_info = printer_info
)

# Main control loop
while True:
    # Send the API request
    response = client.infer(payload=payload)
    print(response)

    # Insert custom post-processing

    # Wait 10.0 seconds
    sleep(10.0)
