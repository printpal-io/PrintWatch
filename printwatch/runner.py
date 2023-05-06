from .client import *
from .utils import *
from .interface import *
from uuid import uuid4
from initializers import *
import asyncio
import time
from copy import deepcopy




class Runner:
    '''
    This is the main object that controls monitoring loops
    that are being ran.

    '''
    def __init__(
            self,

        ):
        self.api = API()
        self.api_thread = self.api.spawn_process()
        self._runner = Scheduler(
                            interval=10.0,
                            callback=self._scan
                        )
        self.aio = asyncio.get_event_loop()
        self.aio.run_forever()



    async def _scan(self):
        '''
        Runs the loop at the set interval
        '''
        try:
            await asyncio.sleep(self.scan_interval)
        except Exception as e:
            print('{}'.format(str(e)))

    def _scan_sync(self):
        '''
        Runs the loop at the set interval in synchronous fashion
        '''
        try:
            sleep(self.scan_interval)

        except Exception as e:
            print('{}'.format(str(e)))
