import aiohttp
import requests
from .utils import *
from base64 import b64encode
from typing import List, Union
import aiohttp


class PrintWatch():
    def __init__(
            self,
            api_key : str,
            stream : str = None,
            ssl : bool = True,
            source : str = None
        ):
        self.route = 'https://ai.printpal.io' if ssl else 'http://ai.printpal.io'
        self.printer_info = init_default(api_key=api_key)
        self.loader = DataLoader(source)

    def _create_payload(
            self,
            encoded_image : Union[bytearray, str],
        ):
        payload = self.printer_info.payload
        if isinstance(encoded_image, bytearray):
            encoded_image = b64encode(encoded_image).decode('utf8')
        payload['image_array'] = encoded_image

        return payload

    def _send(
        self,
        endpoint : str,
        payload : dict
    ):
        r = requests.post(
                '{}/{}'.format(self.route, endpoint),
                json = payload,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout = 10.0
            ).json()
        if r.get('detail') is not None:
            raise InferencePayloadError(r)
        return r

    async def _send_async(
                self,
                endpoint : str,
                payload : dict
            ):
            async with aiohttp.ClientSession() as session:
                async with session.post(
                                '{}/{}'.format(self.route, endpoint),
                                json = payload,
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=aiohttp.ClientTimeout(total=10.0)
                            ) as response:
                            r = await response.json()
            return r

    def set_source(self, value):
        self.loader.source = value
        if 'http' in value:
            self.loader.type = 'http'
        else:
            self.loader.type = 'file'

    def infer(
            self,
            image : Union[bytearray, str]
        ):
        if self.printer_info['api_key'] in [None, '']:
            raise APIKeyError()

        if isinstance(image, str):
            # should be a file name
            image = self.loader.open(image)

        return self._send(
                        endpoint='api/v2/infer',
                        payload=self._create_payload(image)
                )

    async def async_infer(
                self,
                image : Union[bytearray, str] = None
        ):
        if self.printer_info['api_key'] in [None, '']:
            raise APIKeyError()

        if image is None:
            image = await self.loader.async_open(self.loader.source)
        elif isinstance(image, str):
            # should be a file name
            image = await self.loader.async_open(image)
        r = await self._send_async(
                        endpoint='api/v2/infer',
                        payload=self._create_payload(image)
                )

        self.response = r
