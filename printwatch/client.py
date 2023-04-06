import aiohttp
import requests
from .utils import PrinterInfo
from base64 import b64encode



class PrintWatchClient():
    def __init__(
            self,
            stream=None,
            ssl : bool = True
        ):
        self.route = 'https://ai.printpal.io' if ssl else 'http://ai.printpal.io'

    def _create_payload(
            self,
            encoded_image,
            printer_info : PrinterInfo
        ):
        payload = printer_info.payload
        if isinstance(encoded_image, bytearray):
            encoded_image = b64encode(encoded_image).decode('utf8')
        payload['image_array'] = encoded_image

        return payload


    def infer(self, payload):
        return self._send(endpoint='api/v2/infer', payload=payload)

    def _send(
        self,
        endpoint,
        payload
    ):
        r = requests.post(
                '{}/{}'.format('https://ai.printpal.io', endpoint),
                json = payload,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        self.response = r.json()
        return self.response

    async def _send_async(
                self,
                endpoint,
                payload
            ):

            async with aiohttp.ClientSession() as session:
                async with session.post(
                                '{}/{}'.format('https://ai.printpal.io', endpoint),
                                json = payload,
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=aiohttp.ClientTimeout(total=10.0)
                            ) as response:
                            r = await response.json()
            self.response = r
            return r
