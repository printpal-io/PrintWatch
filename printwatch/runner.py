from .client import *
from .utils import *
from uuid import uuid4
import asyncio
import time




class Runner:
    '''
    This is the main object that controls monitoring loops
    that are being ran.

    '''
    def __init__(
            self,

        ):
        self.monitors = []
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

    def add_monitor(
            self,
            api_key : str,
            printer_id : str = uuid4().hex,
            api_client : PrintWatchClient = None,
            source : str : None
        ):
        if api_client is None:
            api_client = PrintWatch(
                                api_key=api_key,
                                printer_id=printer_id,
                                source=source
                            )

        loop = LoopHandler(api_client)

        self.monitors.append(
            [
                uuid4().hex,
                loop = loop
                Scheduler(
                    callback = loop._run_once
                )
            ]
        )
