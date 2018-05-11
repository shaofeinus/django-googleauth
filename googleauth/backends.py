import logging

from django.contrib.auth.models import User

from googleauth.models import GoogleCreds
from sheets import services


class GoogleAuthBackend:

    def authenticate(self, request, email=None, credentials=None):
        if email is None:
            logging.debug('No email')
            return None
        if credentials is None:
            logging.debug('No credentials')
            return None
        if not credentials.valid:
            logging.debug('Credentials not valid')
            return None
        if credentials.expired:
            logging.debug('Credentials expired')
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
            logging.debug('Creating new user {}'.format(email))
            user = User(username=email, email=email)
            user.save()
            # Create corresponding google credentials
            GoogleCreds(user=user, credentials=credentials).save()
            # Create corresponding sheets meta info
            meta_spreadsheet, error_status = services.create_meta_spreadsheet(user)
            if error_status is not None:
                logging.error('Error status {} when trying to create meta spreadsheet'.format(error_status))
                return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None