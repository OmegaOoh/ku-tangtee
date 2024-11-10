"""logger module for logging activities app."""
import logging
from django.contrib.auth.models import User


logger = logging.getLogger('activities')


def convert_to_log_msg(req_user: User, action: str, act_id: int, target_user: User = None, reason: str = None):
    """Convert parameters into log message.

    :param req_user: request user
    :param action: action of the request user
    :param act_id: activity id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    req_user_str: str = f'User {req_user.id} ({req_user.first_name})'
    act_str: str = f'Activity {act_id}' if act_id != -1 else 'Activity'
    target_user: str = f' User {target_user.id} ({target_user.first_name})' if target_user else ''
    reason: str = f' ({reason})' if reason else ''

    return f'{req_user_str} {action}{target_user} {act_str}{reason}'


def info(req_user: User, action: str, activity_id: int = -1, target_user: User = None, reason: str = None):
    """Log INFO level messages in activities app.

    :param req_user: request user
    :param action: action of the request user
    :param activity_id: activity id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    msg = convert_to_log_msg(req_user, action, activity_id, target_user, reason)
    logger.info(msg)


def warning(req_user: User, action: str, activity_id: int = -1, target_user: User = None, reason: str = None):
    """Log WARNING level messages in activities app.

    :param req_user: request user
    :param action: action of the request user
    :param activity_id: activity id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    msg = convert_to_log_msg(req_user, action, activity_id, target_user, reason)
    logger.warning(msg)
