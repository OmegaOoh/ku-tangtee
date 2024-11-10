"""logger module for logging profiles app."""
import logging
from django.contrib.auth.models import User


logger = logging.getLogger('profiles')


def convert_to_log_msg(req_user: User, action: str, profile_id: int = -1, target_user: User = None, reason: str = '') -> str:
    """Convert parameters into log message.

    :param req_user: request user
    :param action: action of the request user
    :param profile_id: profile id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    req_user_str = f'User {req_user.id} ({req_user.first_name})'
    profile_str = f'Profile {profile_id}' if profile_id != -1 else 'Profile'
    target_user = f' User {target_user.id} ({target_user.first_name})' if target_user else ''
    reason = f' ({reason})' if reason else ''

    return f'{req_user_str} {action}{target_user} {profile_str}{reason}'


def info(req_user: User, action: str, profile_id: int = -1, target_user: User = None, reason: str = '') -> None:
    """Log INFO level messages in profiles app.

    :param req_user: request user
    :param action: action of the request user
    :param profile_id: profile id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    msg = convert_to_log_msg(req_user, action, profile_id, target_user, reason)
    logger.info(msg)


def warning(req_user: User, action: str, profile_id: int = -1, target_user: User = None, reason: str = '') -> None:
    """Log WARNING level messages in profiles app.

    :param req_user: request user
    :param action: action of the request user
    :param profile_id: profile id, -1 if not specify
    :param target_user: target user of the action
    :param reason: reason or note of the action
    """
    msg = convert_to_log_msg(req_user, action, profile_id, target_user, reason)
    logger.warning(msg)
