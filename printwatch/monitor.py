






class LoopHandler:
    '''
    Controls the general loop logic for making API requests to the
    PrintWatch API, handles the buffers, and action taking.
    '''
    def __init__(
            self,
            api_client : PrintWatchClient,
            MULTIPLIER : float = 4.0
        ):

        self.MULTIPLIER = MULTIPLIER
        self._buffer = [[0, 0, 0]] * self._buffer_length
        self._scores = [0] * int(self._buffer_length * self.MULTIPLIER)
        self._levels = [False, False]


    async def _run_once(self):
        '''
        Runs one loop of the cycle. This method is a callback for the asynchronous loop
        '''

        try:
            if self.run_function:
                await self._camera.snap()

                response = await _async_infer(
                                    b64encode(frame).decode('utf8'),
                                )
                if response.get('statusCode') == 200:
                    '''
                    replace this
                    handle_buffer(
                                buffer : List[List[float]],
                                scores : List[float],
                                levels : List[bool],
                                score : float,
                                smas : List[float],
                                new_levels : List[float],
                                buffer_length : int,
                                MULTIPLIER : int
                        )
                    '''

                    handle_buffer(
                                score=response.get("score"),
                                smas=response.get("smas")[0],
                                levels=response.get("levels")
                        )
                    await self._handle_action()
        except Exception as e:
            print(str(e))
