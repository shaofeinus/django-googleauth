from django.conf import settings


def _get_setting(setting_name, default):
    return getattr(settings, setting_name, default)


GOOGLEAUTH_SUCCESS_VIEW = _get_setting('GOOGLEAUTH_SUCCESS_VIEW', 'googleauth-auth-success')
GOOGLEAUTH_ERROR_VIEW = _get_setting('GOOGLEAUTH_ERROR_VIEW', 'googleauth-auth-error')
