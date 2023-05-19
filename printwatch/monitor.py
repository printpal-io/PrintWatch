

class LoopHandler:
    '''
    Controls the general loop logic for making API requests to the
    PrintWatch API, handles the buffers, and action taking.
    '''
    def __init__(
            self,
            api_client : PrintWatchClient,
            settings : dict = {
                                    'pause_print' : False,
                                    'action' : None,
                                    'notifications' : False,
                                    'trigger_condition' : None
                                }
            buffer_length : int = 16,
            MULTIPLIER : float = 4.0
        ):

        self.MULTIPLIER = MULTIPLIER
        self._buffer_length = buffer_length
        self._buffer = [[0, 0, 0]] * self._buffer_length
        self._scores = [0] * int(self._buffer_length * self.MULTIPLIER)
        self._levels = [False, False]
        self._api_client = api_client
        self._settings = settings


    async def _run_once(self):
        '''
        Runs one loop of the cycle. This method is a callback for the asynchronous loop
        '''

        try:
            if self.run_function:
                response = await self._api_client.async_infer()
                if response.get('statusCode') == 200:

                    self._buffer, self._scores, self._levels = handle_buffer(
                                                                    buffer=self._buffer,
                                                                    scores=self._scores,
                                                                    levels=self._levels,
                                                                    score=response.get("score"),
                                                                    smas=response.get("smas")[0]
                                                                    new_levels=response.get("levels"),
                                                                    buffer_length=self._buffer_length,
                                                                    MULTIPLIER=self.MULTIPLIER
                                                                )
                    enum, action, notif = await handle_action(
                                                levels=self._levels,
                                                pause_print=settings.get("pause_print"),
                                                action_method=settings.get("action"),
                                                notifications=settings.get("notifications")
                                            )
                    '''
                    Logic to handle what happens after a notification/pause/cancel
                    needs to be added here on a case-by-case basis.

                    State handling utilizes the enum returned by the action handler.
                    Where the enum values correspond to:
                    0 - Action attemped and notification[action] send attempted. | action = result of pause action | notif = result of notification send
                    1 - Ation attempted. | action = result of pause action | notif = None
                    2 - Notification[warning] send attempted | action = None | notif = result of notification send
                    3 - None actions taken
                    '''
        except Exception as e:
            print(str(e))
