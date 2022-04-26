from urllib.request import Request, urlopen
from json import loads, dumps
from uuid import uuid4
from threading import Lock
from base64 import b64encode



class PrintWatchClient():
    def __init__(self, stream=None):
        self.parameters = {}
        self.stream = stream
        self.route = 'http://printwatch-printpal.pythonanywhere.com'

    def _load_stream(self, source):
        self.stream = source

    def _create_payload(self, image):
        self.parameters['image_array'] = image
        if len(self.parameters) < 1:
            self._dummy()
        return dumps(self.parameters).encode('utf8')

    def _dummy(self, api_key):
        self.parameters = {
            'settings': {
                'enable_email_notification': False,
                'confidence': 60,
                'enable_feedback_images': True,
                'api_key': api_key
            },
            'parameters': {
                'last_t': 0.0,
                'ip': '127.0.0.1',
                'nms': False,
                'id': uuid4().hex
            },
            'job': {
                'file': {
                    'name': 'Dummy-file'
                }
            },
            'data': {
                'progress': {
                    'printTime': 500,
                    'completion': 10.1,
                    'printTimeLeft': 10
                }
            }
        }

    def _send_request(self, frame=None):
        _inference_image = self._get_frame(frame)
        return self._load(self._request(_inference_image))


    def _request(self, image):
        return Request(f'{self.route}/inference/', data=self._create_payload(image), method='POST')

    def _load(self, _request=None):
        if _request is None:
            return False
        return loads(urlopen(_request).read())

    def _get_frame(self, frame=None):
        if frame is None and self.stream is not None:
            with Lock():
                #stream will need to be an object
                return self.stream.frame

        return b64encode(frame).decode('utf8')

    def send_infer(self, image, api_key, parameters=None):
        if parameters is None:
            self._dummy(api_key)
        else:
            self.parameters = parameters
        return self._send_request(image)


class CVClient():
    def __init__(self, stream=None):
        self.parameters = {}
        self.stream = stream
        self.route = 'http://printwatch-printpal.pythonanywhere.com'

    def _load_stream(self, source):
        self.stream = source

    def _create_payload(self, image):
        self.parameters['image_array'] = image
        if len(self.parameters) < 1:
            self._dummy()
        return dumps(self.parameters).encode('utf8')

    def _dummy(self, api_key):
        self.parameters = {
            'parameters': {
                'nms': False,
                'confidence': 60,
                'model': 'yolov5s',
                'size': 640
            },
            'tokens': {
                'enable_feedback_images': True,
                'api_key': api_key,
            }
        }

    def _send_request(self, frame=None):
        _inference_image = self._get_frame(frame)
        return self._load(self._request(_inference_image))


    def _request(self, image):
        return Request(f'{self.route}/inference/', data=self._create_payload(image), method='POST')

    def _load(self, _request=None):
        if _request is None:
            return False
        return loads(urlopen(_request).read())

    def _get_frame(self, frame=None):
        if frame is None and self.stream is not None:
            with Lock():
                #stream will need to be an object
                return self.stream.frame

        return b64encode(frame).decode('utf8')

    def send_infer(self, image, api_key, parameters=None):
        if parameters is None:
            self._dummy(api_key)
        else:
            self.parameters = parameters
        return self._send_request(image)
