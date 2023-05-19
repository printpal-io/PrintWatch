from printwatch.client import PrintWatch
from time import sleep


API_KEY = "sub_1My6bNEDu7u6sxLduFwZLh93"
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
