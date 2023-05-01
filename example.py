from printwatch.client import PrintWatch
from printwatch.utils import *
from time import sleep

# Create Client object
client = PrintWatch("sub_1N2V6dEDu7u6sxLdCTwbpC5F")

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
