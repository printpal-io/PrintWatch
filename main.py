import printwatch.client
from printwatch.utils import ImageFileLoader
import os

# Authentication
api_key = 'your_secret_key'
test_image_name = 'test.png'

# Initializing the client
client = printwatch.client.PrintWatchClient()
fl = ImageFileLoader()

fl.load_file(test_image_name)


# Inference
results = client.send_infer(fl._get()[1], api_key)
print(results)
