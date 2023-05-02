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

## Installation

Begin by cloning the repository

```sh
git clone https://github.com/printpal-io/PrintWatch.git
```

Enter the working directory

```sh
cd PrintWatch
```

Install dependencies

```sh
pip install -r requirements.txt
```

## Usage

Create a file and import the printwatch object

```python
from printwatch.client import PrintWatch

# Create Client object
client = PrintWatch("INSERT_API_KEY")

# Main control loop
# on a single image/new image has to be loaded every time
while True:
    # Send the API request
    response = client.infer('img.jpg')
    print(response)

    '''
    # Insert custom post-processing logic here
    # A base template will be added to this toolbox shortly
    '''
    # Wait 10.0 seconds
    sleep(10.0)
```

## Example code

The examples folder contains boilerplate code for a few common use cases and can found in [examples](https://github.com/printpal-io/PrintWatch/tree/main/examples). It includes code for:

* Defect detection on image files
* Defect detection on a webcam (HTTP) stream
* Asynchronous defect detection on a webcam (HTTP) stream
* Integrating defect detection into your server or cloud system
