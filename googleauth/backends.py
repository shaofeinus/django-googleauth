import logging

from django.contrib.auth.models import User

from .models import GoogleCreds

logger = logging.getLogger(__name__)


class GoogleAuthBackend:

    def authenticate(self, request, email=None, credentials=None):
        if email is None:
            logger.info('No email')
            return None
        if credentials is None:
            logger.info('No credentials')
            return None
        if not credentials.valid:
            logger.info('Credentials not valid')
            return None
        if credentials.expired:
            logger.info('Credentials expired')
            return None
        try:
            # Get user
            user = User.objects.get(username=email)
            # Update credentials
            goog_creds = user.googlecreds
            goog_creds.credentials = credentials
            goog_creds.save(update_fields=['credentials'])
        except User.DoesNotExist:
            # Create user if does not exist
            logger.debug('Creating new user {}'.format(email))
            user = User(username=email, email=email)
            user.save()
            # Create corresponding google credentials
            GoogleCreds(user=user, credentials=credentials).save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
