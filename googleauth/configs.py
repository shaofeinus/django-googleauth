from django.conf import settings

AUTH_SUCCESS_TEMPLATE = getattr(settings, 'GOOGLEAUTH_AUTH_SUCCESS_TEMPLATE', 'googleauth/auth_success.html')
AUTH_ERROR_TEMPLATE = getattr(settings, 'GOOGLEAUTH_AUTH_ERROR_TEMPLATE', 'googleauth/auth_error.html')
