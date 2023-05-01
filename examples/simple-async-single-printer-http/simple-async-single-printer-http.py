from printwatch.client import PrintWatch
from printwatch.utils import *
from time import sleep
import asyncio

WEBCAM_URL = 'http://localhost:8000/webcam/?action=snapshot'

# Create Client object
client = PrintWatch(
            "INSERT_API_KEY",
            source=WEBCAM_URL
        )

'''
# Main control loop
# on a single image grabbed from the WEBCAM_URL defined above
# the standalone = True enables the scheduler object to automatically
# run the loop.
#
# The response needs to be managed from the Scheduler object
'''

loop = Scheduler(callback=client.async_infer, standalone=True)

'''
#
# To run with standalone = False, use an external async loop controller like:

 loops = []
 for i in range(10):
     loops.append(
         Scheduler(callback=client.async_infer, standalone=False)
     )
 aio = asyncio.get_event_loop()
 aio.run_forever()
#
'''
