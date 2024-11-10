"""Custom serializer validator."""
from rest_framework import status, exceptions, serializers, validators
from .. import models, logger
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

        if not user_profile:
            logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='No profile')
            message = 'User must have profile page before joining an activity'
            raise ForbiddenValidationError(message)

        if not user_profile.able_to_join_more:
            logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='#Join reach limit')
            message = 'The number of activities you have joined has reached the limit'
            raise ForbiddenValidationError(message)

        if act:

            if not act.is_active():
                logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='Not active')
                message = f'The activity {act.name} is not active.'
                raise ForbiddenValidationError(message)

            if act.is_full():
                logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='Full')
                message = f'The activity {act.name} is full.'
                raise ForbiddenValidationError(message)

            if not act.rep_check(user):
                logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='Rep too low')
                message = f'Your reputation score is too low to join {act.name}'
                raise ForbiddenValidationError(message)

        else:

            logger.warning(req_user=user, action='FAIL to JOIN', activity_id=act.id, reason='Activity not exist')
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
            logger.warning(req_user=attrs['user'], action='FAIL to JOIN', activity_id=attrs['activity'].id, reason='Already join')
            raise ForbiddenValidationError(
                {
                    "message": f"You've already joined the activity {attrs['activity'].name}."
                },
                code='unique'
            )
