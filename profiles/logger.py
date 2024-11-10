"""logger module for logging profiles app."""
import logging
from django.contrib.auth.models import User


logger = logging.getLogger('profiles')


def convert_to_log_msg(profile_id, action, reason, req_user, target_user):
    req_user_str: str = f'User {req_user.id} ({req_user.first_name})'
    profile_str: str = f'Profile {profile_id}' if profile_id != -1 else 'Profile'
    target_user: str = f' User {target_user.id} ({target_user.first_name})' if target_user else ''
    reason: str = f' ({reason})' if reason else ''

    return f'{req_user_str} {action}{target_user} {profile_str}{reason}'


def info(req_user: User, action: str, profile_id: int, target_user: User=None, reason: str=None):
    msg = convert_to_log_msg(profile_id, action, reason, req_user, target_user)
    logger.info(msg)


def warning(req_user: User, action: str, profile_id: int, target_user: User=None, reason: str=None):
    msg = convert_to_log_msg(profile_id, action, reason, req_user, target_user)
    logger.warning(msg)
