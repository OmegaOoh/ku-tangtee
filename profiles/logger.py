"""logger module for logging profiles app."""
import logging
from dataclasses import dataclass
from enum import Enum
from django.contrib.auth.models import User


logger = logging.getLogger('profiles')


class Action(Enum):
    """Enum class that store a format string template that contain action."""

    CREATE = "{} CREATE{} {}{}"
    EDIT = "{} EDIT{} {}{}"
    FAIL_CREATE = "{} FAIL to CREATE{} {}{}"
    TRY_EDIT = "{} TRY to EDIT{} {}{}"


@dataclass
class RequestData:
    """Data class that stores user, target user, and profile data from request action.

    :param req_user: request user
    :param profile_id: activity id, -1 if not specify
    :param target_user: target user of the action
    """

    req_user: User
    profile_id: int
    target_user: User = None


def data_to_log(action: Action, data: RequestData, reason: str = '') -> str:
    """Convert parameters into log message.

    :param action: action of the request user
    :param data: the request user, target user, and activity data from request action
    :param reason: reason or note of the action
    """
    req_user_str = f'User {data.req_user.id} ({data.req_user.first_name})'
    act_str = f'Profile {data.profile_id}' if data.profile_id != -1 else 'Profile'
    target_user = f' User {data.target_user.id} ({data.target_user.first_name})' if data.target_user else ''
    reason = f' ({reason})' if reason else ''

    return action.value.format(req_user_str, target_user, act_str, reason)
