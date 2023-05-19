import time
from typing import Union, List


def handle_buffer(
            buffer : List[List[float]],
            scores : List[float],
            levels : List[bool],
            score : float,
            smas : List[float],
            new_levels : List[float],
            buffer_length : int,
            MULTIPLIER : int
    ) -> tuple:
    '''
    Manages the buffer, scores, and levels.

    '''
    buffer.append(smas)
    scores.append(score)
    levels = new_levels

    while len(buffer) > buffer_length:
        buffer.pop(0)

    while len(scores) > buffer_length * MULTIPLIER:
        scores.pop(0)

    return buffer, scores, levels


def default_condition(
        notify_conditions : List = [True],
        action_conditions : List = [True],
        type : str = 'notify'
    ):
    '''
    Checks if a trigger action should be permitted

    Inputs:
    - type : str - the type of trigger to check for

    Returns:
    - valid : Boolean - whether a certain trigger should be allowed
    '''
    if type == 'notify':
        return True if ([condition for condition in notify_conditions].count(False) == 0) else False
    elif type == 'action':
        return True if ([condition for condition in action_conditions].count(False) == 0) else False

def last_n_notifications_interval(
        self,
        buffer : List[float], # buffer is a list of the time.time() values when notifications are sent
        interval : int = 1 * 60 * 60 # default 1-hour
    ) -> int:
    '''
    Checks how many notifications have been sent in the last N hours

    Inputs:
    - interval : int - the interval to check occurences of notifications

    Returns:
    - running_total : int - number of notifications in the last N hours
    '''
    # 4 hour default interval
    current_time = time()
    running_total = 0

    # reverse-order because self._notificationsSent values get appended
    for idx in reversed(range(len(buffer))):
        if time() - buffer[idx] > interval:
            break
        running_total += 1
    return running_total



async def handle_action(
        levels : List[bool],
        trigger_condition = default_condition,
        pause_print : bool = False,
        action_method = None,
        notifications : bool = False
    ) -> tuple:
    '''
    Checks if any actions should be taken.
    Notifications and Pauses will be triggered from inside this method.
    '''

    if levels[1] and trigger_condition('action') and pause_print:
        # Currently no way of supporting actions via serial.
        # Only supported over ethernet/IP
        notification_level = 'action'

        # Take the pause action if enabled
        action_result = action_method()

        if notifications:
            response = await async_notify(
                                    notification_level=notification_level
                                )
            return 0, action_result, response

        return 1, action_result, None

    elif levels[0] and trigger_condition('notify'):
        notification_level = 'warning'

        response = await async_notify(
                                notification_level=notification_level
                            )
        return 2, None, response
    return 3, None, None
