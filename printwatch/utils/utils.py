import PIL.Image as Image
from PIL import ImageDraw
from io import BytesIO
import os
from uuid import uuid4
from base64 import b64encode
import requests
import asyncio
import aiohttp

class PrinterInfo:

    def __init__(
        self,
        api_key : str = '',
        printer_id : str = uuid4().hex,
        ticket_id : str = uuid4().hex
        ):
        self.payload = {
            'api_key' : api_key,
            'printer_id' : printer_id,
            'ticket_id' : ticket_id,
            'version' : '1.2.11',
            'state' : 0,
            'conf' : 60,
            'buffer_length' : 16,
            'buffer_percent' : 60,
            'thresholds' : [0.30, 0.60],
            'scores' : [],
            'sma_spaghetti' : 0,
            'enable_feedback_images' : True
        }

    def __getitem__(self, key):
        return self.payload.get(key)

    def __setitem__(self, key, value):
        self.payload[key] = value

    def create_ticket(self):
        self.payload['ticket_id'] = uuid4().hex

    def clear_ticket(self):
        self.payload['ticket_id'] = ''

    def update_job_info(
            self,
            state : int,
            printTime : float,
            printTimeLeft : float,
            progress : float,
            job_name : str
        ):
        self.payload['state'] = state
        self.payload['printTime'] = printTime
        self.payload['printTimeLeft'] = printTimeLeft
        self.payload['progress'] = progress
        self.payload['job_name'] = job_name

class DataLoader:

    def __init__(self, source):
        self.data = None
        self.source = source
        self.type = ''

    def _load(self, file):
        with open(file, 'rb') as f:
            return bytearray(f.read())

    def _get(
            self,
            timeout : float = 10.0
        ):
        response = requests.get(
            '{}'.format(self.source),
            timeout=timeout
            )
        if response.status_code == 200:
            return b64encode(response.content).decode('utf8')
        else:
            raise HTTPgetError(response.content)

    async def _async_get(
                self,
                timeout : float = 10.0
        ):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                            '{}'.format(
                                self.source
                            ),
                            timeout=aiohttp.ClientTimeout(total=timeout)
                        ) as response:
                        if response.status == 200:
                            image = await response.read()
                            return bytearray(image)
                        else:
                            raise HTTPgetError(response.content)

    def open(
            self,
            location : str
        ):

        if location in [None, '']:
            return

        if os.path.isfile(location):
            self.type = 'file'
            return self._load(location)
        elif 'http' in location:
            self.type = 'http'
            if self.source is None or self.source is not location:
                self.source = location
            return self._get()

    async def async_open(
            self,
            location : str
        ):

        if location in [None, '']:
            return

        if os.path.isfile(location):
            self.type = 'file'
            return self._load(location)
        elif 'http' in location:
            self.type = 'http'
            if self.source is None or self.source is not location:
                self.source = location
            r = await self._async_get()
            return r





class Scheduler:
    def __init__(
            self,
            interval : float = 10.0,
            callback = None,
            standalone : bool = False
        ):
        '''
        Handles the scheduling of the loop.
        Controls the asynchronous callback in the LoopHandler object
        '''

        self._interval = interval
        self.task = asyncio.ensure_future(self._run_loop())
        self._run = True
        self._callback = callback
        if not standalone:
            self.run()

    async def _run_loop(self):
        '''
        Runs the loop.
        Basic sleep function for the inference call interval (default 10.0s), then
        the Inference and handing
        '''
        try:
            while self._run:
                await asyncio.sleep(self._interval)
                await self._callback()
        except asyncio.CancelledError:
            print("Cancelled")
        except Exception as e:
            self._restart_loop()

    def set_interval(
            self,
            value : float = 10.0
        ):
        self._interval = value

    def _restart_loop(self):
        # Cleanup first
        self._run = False
        self.cancel()
        self.task = None

        # Re-start the task
        self._run = True
        self.task = asyncio.ensure_future(self._run_loop())

    def cancel(self):
        self._run = False
        self.task.cancel()

    def run(self):
        asyncio.get_event_loop().run_forever()

class ROI():
    def _get_cropped_area(image, coords : tuple):
        #image must be an Image object
        return image.crop(coords)

    def get_cropped_areas(image, regions : list):
        return [_get_cropped_area(image, region) for region in regions]

    def preview_slices(image, regions):
        base_image = ImageDraw.Draw(image)

        slices = get_cropped_areas(image, regions)
        for ele in slices:
            idx = slices.index(ele)

            base_image.rectangle([(regions[idx][0], regions[idx][1]), (regions[idx][2], regions[idx][3])], fill = None, outline = 'red', width = int(ceil(0.002 * sqrt(image.size[0] * image.size[1]))))
            ele.show()
        image.show()

class APIKeyError(Exception):
    def __init__(self):
        super().__init__('API Key is Invalid')

class HTTPgetError(Exception):
    def __init__(self, e):
        super().__init__(f'Unable to get HTTP stream: {e}')

class InferencePayloadError(Exception):
    def __init__(self, e):
        super().__init__(f'Invalid inference payload: {e}')

def init_default(api_key : str) -> PrinterInfo:
    info = PrinterInfo(api_key=api_key)
    info.update_job_info(
        state = 0,
        printTime = 600,
        printTimeLeft = 100,
        progress = 85.7,
        job_name = 'dummy.stl'
    )
    return info
