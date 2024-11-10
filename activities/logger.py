"""logger module for logging activities app."""
import logging
from django.contrib.auth.models import User


logger = logging.getLogger('activities')


def convert_to_log_msg(act_id, action, reason, req_user, target_user):
    req_user_str: str = f'User {req_user.id} ({req_user.first_name})'
    act_str: str = f'Activity {act_id}' if act_id != -1 else 'Activity'
    target_user: str = f' User {target_user.id} ({target_user.first_name})' if target_user else ''
    reason: str = f' ({reason})' if reason else ''

    return f'{req_user_str} {action}{target_user} {act_str}{reason}'


def info(req_user: User, action: str, activity_id: int, target_user: User=None, reason: str=None):
    msg = convert_to_log_msg(activity_id, action, reason, req_user, target_user)
    logger.info(msg)


def warning(req_user: User, action: str, activity_id: int, target_user: User=None, reason: str=None):
    msg = convert_to_log_msg(activity_id, action, reason, req_user, target_user)
    logger.warning(msg)
