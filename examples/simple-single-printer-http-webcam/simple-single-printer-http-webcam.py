from printwatch.client import PrintWatch
from time import sleep

# Create Client object
client = PrintWatch("INSERT_API_KEY")

# Define the camera's snapshot endpoint
WEBCAM_URL = 'http://localhost:8000/webcam/?action=snapshot'

# Main control loop
# on a single image grabbed from the WEBCAM_URL defined above
while True:
    # Send the API request
    response = client.infer(WEBCAM_URL)
    print(response)

    '''
    # Insert custom post-processing logic here
    # A base template will be added to this toolbox shortly
    '''
    # Wait 10.0 seconds
    sleep(10.0)
