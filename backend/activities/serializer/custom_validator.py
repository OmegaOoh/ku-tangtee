"""Custom serializer validator."""
from rest_framework import status, exceptions, serializers, validators
from .. import models
from ..logger import logger, Action, RequestData, data_to_log
from django.contrib.auth.models import User
from typing import Any


class ForbiddenValidationError(exceptions.APIException):
    """Custom error inherit from ValidationError but different error code."""

    status_code = status.HTTP_403_FORBIDDEN


class CanJoinValidator:
    """Validate activity joinability."""

    def __call__(
        self,
        attrs: dict[str, models.Activity],
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Raise an error if activity is unjoinable.

        :param attrs: Dict contain instance of each fields.
        :raises ForbiddenValidationError: If activity is unjoinable.
        :return: None
        """
        act: models.Activity = attrs['activity']
        user: User = attrs['user']
        user_profile = user.profile_set.first()

        req_data = RequestData(req_user=user, act_id=(act.id if act else -1))

        if not user_profile:
            logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'No profile'))
            message = 'User must have profile page before joining an activity'
            raise ForbiddenValidationError(message)

        if not user_profile.able_to_join_more:
            logger.warning(data_to_log(Action.FAIL_JOIN, req_data, '#Join reach limit'))
            message = 'The number of activities you have joined has reached the limit'
            raise ForbiddenValidationError(message)

        if act:

            if not act.is_active():
                logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'Not active'))
                message = f'The activity {act.name} is not active.'
                raise ForbiddenValidationError(message)

            if act.is_full():
                logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'Full'))
                message = f'The activity {act.name} is full.'
                raise ForbiddenValidationError(message)

            if not act.rep_check(user):
                logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'Rep too low'))
                message = f'Your reputation score is too low to join {act.name}'
                raise ForbiddenValidationError(message)

        else:

            logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'Activity not exist'))
            message = 'Activity not exist'
            raise ForbiddenValidationError(message)

        return None


class CustomMsgUniqueTogetherValidator(validators.UniqueTogetherValidator):
    """Custom validator class base from UniqueTogetherValidator."""

    status_code = status.HTTP_403_FORBIDDEN

    def __call__(self, attrs: dict[str, Any], serializer: serializers.Serializer) -> Any:
        """Validate data such that user can't join activity that they've join.

        :param attrs: Dict contain instance of each field.
        :raises ForbiddenValidationError: If user id and activity id combination are not unique.
        :return: None
        """
        try:
            return super().__call__(attrs, serializer)
        except validators.ValidationError:
            req_data = RequestData(req_user=attrs['user'], act_id=attrs['activity'].id)
            logger.warning(data_to_log(Action.FAIL_JOIN, req_data, 'Already join'))
            raise ForbiddenValidationError(
                {
                    "message": f"You've already joined the activity {attrs['activity'].name}."
                },
                code='unique'
            )
