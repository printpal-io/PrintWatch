import PIL.Image as Image
from PIL import ImageDraw
from math import sqrt, ceil
import asyncio
from uuid import uuid4

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



class Scheduler:
    def __init__(
            self,
            interval
        ):
        self.interval = interval
        self.task = asyncio.ensure_future(self._wait_interval())

    async def _wait_interval(self):
        await asyncio.sleep(self.interval)

    def cancel(self):
        self.task.cancel()

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
