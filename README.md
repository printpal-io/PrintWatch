<p align="center">
    <br>
    <img src="https://printpal.io/wp-content/uploads/2022/01/printwatch_logo_gh.png" width="600"/>
    <br>
<p>
<p align="center">
    <a href="https://printpal.io/">
        <img alt="Documentation" src="https://img.shields.io/badge/website-online-brightgreen">
    </a>
    <a href="https://github.com/printpal-io/OctoPrint-PrintWatch/releases">
        <img alt="GitHub release" src="https://img.shields.io/badge/release-1.2.11-blue">
    </a>
    <a href="https://printpal.pythonanywhere.com/api/status">
        <img alt="API Status" src="https://img.shields.io/badge/API-online-brightgreen">
    </a>
    <a href="https://discord.gg/DRM7w88AbS">
        <img alt="Discord Server" src="https://img.shields.io/badge/discord-online-blueviolet?logo=discord">
    </a>
</p>
<h3 align="center">
  PrintWatch API
</h3>
<p>
  PrintWatch uses Artificial Intelligence to monitor your 3D prints for any defects that begin to form. The plugin takes the video feed from any camera and runs it through a Machine Learning model that detects print defects in real-time. This repository is for custom integrations of the API, if you are using OctoPrint, refer to the <a href="https://github.com/printpal-io/OctoPrint-PrintWatch">OctoPrint-PrintWatch repository</a>
</p>


<details open>
<summary>Inference</summary>

```python
from printwatch.client import PrintWatchClient
from printwatch.utils import *
from time import sleep

# Insert API key
printer_info = init_default("api_key")

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
```
</details>
