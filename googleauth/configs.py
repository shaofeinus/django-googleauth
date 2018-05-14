from django.conf import settings

GOOGLEAUTH_SUCCESS_VIEW = getattr(settings, 'GOOGLEAUTH_SUCCESS_VIEW', 'googleauth-auth-success')
GOOGLEAUTH_ERROR_VIEW = getattr(settings, 'GOOGLEAUTH_ERROR_VIEW', 'googleauth-auth-error')
