"""logger module for logging activities app."""
import logging
from dataclasses import dataclass
from enum import Enum

from django.contrib.auth.models import User

logger = logging.getLogger('activities')


class Action(Enum):
    """Enum class that store a format string template that contain action."""

    CREATE = "{} CREATE{} {}{}"
    JOIN = "{} JOIN{} {}{}"
    LEAVE = "{} LEAVE{} {}{}"
    EDIT = "{} EDIT{} {}{}"
    KICK = "{} KICK{} {}{}"
    EDIT_HOST = "{} EDIT HOST ACCESS to{} {}{}"
    CHECKIN = "{} CHECK-IN to{} {}{}"
    OPEN_CHECKIN = "{} OPEN CHECK-IN for{} {}{}"
    CLOSE_CHECKIN = "{} CLOSE CHECK-IN for{} {}{}"
    FAIL_CREATE = "{} FAIL to CREATE{} {}{}"
    FAIL_JOIN = "{} FAIL to JOIN{} {}{}"
    FAIL_EDIT = "{} FAIL to EDIT{} {}{}"
    FAIL_EDIT_HOST = "{} FAIL to EDIT HOST ACCESS to{} {}{}"
    FAIL_CHECKIN = "{} FAIL to CHECK-IN to{} {}{}"
    FAIL_OPEN_CHECKIN = "{} FAIL to OPEN CHECK-IN for{} {}{}"


@dataclass
class RequestData:
    """Data class that stores user, target user, and activity data from request action.

    :param req_user: request user
    :param act_id: activity id, -1 if not specify
    :param target_user: target user of the action
    """

    req_user: User
    act_id: int
    target_user: User = None


def data_to_log(action: Action, data: RequestData, reason: str = '') -> str:
    """Convert parameters into log message.

    :param action: action of the request user
    :param data: the request user, target user, and activity data from request action
    :param reason: reason or note of the action
    """
    req_user_str = f'User {data.req_user.id} ({data.req_user.first_name})'
    act_str = f'Activity {data.act_id}' if data.act_id != -1 else 'Activity'
    target_user = f' User {data.target_user.id} ({data.target_user.first_name})' if data.target_user else ''
    reason = f' ({reason})' if reason else ''

    return action.value.format(req_user_str, target_user, act_str, reason)
