from urllib.request import Request, urlopen
from json import loads, dumps
from uuid import uuid4
from threading import Lock
from base64 import b64encode



class PrintWatchClient():
    def __init__(self, stream=None):
        self.parameters = []
        self.stream = stream
        self.route = 'http://printwatch-printpal.pythonanywhere.com'

    def _load_stream(self, source):
        self.stream = source

    def _create_payload(self, image, idx=-1):
        try:
            self.parameters[idx]
        except:
            return

        self.parameters[idx]['image_array'] = image
        return dumps(self.parameters[idx]).encode('utf8')

    def _dummy(self, api_key):
        self.parameters.append(
         {
            'scores' : [],
            'version' : '1.1.111',
            'settings': {
                'enable_email_notification': False,
                'confidence': 60,
                'enable_feedback_images': True,
                'api_key': api_key,
                'email_addr' : '',
                'buffer_percent' : 60,
                'buffer_length' : 8
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
        )

    def _send_request(self, frame=None, idx=-1):
        _inference_image = self._get_frame(frame)
        return self._load(self._request(_inference_image, idx))


    def _request(self, image, idx=-1):
        return Request(f'{self.route}/inference/', data=self._create_payload(image, idx), method='POST')

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

    def send_infer(self, image, api_key, parameters=None, idx=-1):
        if parameters is not None:
            if index >= 0:
                self.parameters[idx] = parameters
            else:
                self.parameters.append(parameters)
        else:
            if idx < 0 or len(self.parameters) < idx + 1:
                self._dummy(api_key)
        return self._send_request(image, idx)
