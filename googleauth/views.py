import logging

import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .configs import AUTH_SUCCESS_TEMPLATE, AUTH_ERROR_TEMPLATE

logger = logging.getLogger(__name__)


# Step 1 - Authenticate OAuth
@require_GET
def auth(request):
    next_url = request.GET.get('next', reverse('googleauth-auth-success'))
    if request.user.is_authenticated:
        # User already logged in, redirect to next url
        return redirect(next_url)
    # Authenticate
    flow = _google_flow(request)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=next_url)
    return redirect(authorization_url)


# Step 2 - Save authenticated credentials and log in
@require_GET
def auth_redirect(request):
    response_url = request.get_full_path()
    error = request.GET.get('error')
    code = request.GET.get('code')
    if error is not None:
        # Go to error page if authentication failed
        error_message = 'Authentication error: {}'.format(error)
        logger.info(error_message)
        return _redirect_to_auth_error(error_message, response_url)
    if code is None:
        # Go to error page if authentication code not found
        error_message = 'Authentication code not found'
        logger.info(error_message)
        return _redirect_to_auth_error(error_message, response_url)
    # Get credentials
    flow = _google_flow(request)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Get user email
    service = googleapiclient.discovery.build('plus', 'v1', credentials=credentials)
    me = service.people().get(userId='me').execute()
    email = list(filter(lambda email_info: email_info['type'] == 'account', me['emails']))[0]['value']
    # Login
    user = authenticate(request, email=email, credentials=credentials)
    if user is not None:
        auth_login(request, user)
        # Redirect to url specified in state
        return redirect(request.GET.get('state'))
    else:
        # Redirect to login if authentication failed
        error_message = 'No user returned from login'
        return _redirect_to_auth_error(error_message, response_url)


# Authentication success page
@require_GET
def auth_success(request):
    return render(request, AUTH_SUCCESS_TEMPLATE, {})


# Authentication error page
@require_GET
def auth_error(request):
    return render(
        request, AUTH_ERROR_TEMPLATE,
        {
            'error_message': request.GET.get('error_message', 'Unknown error'),
            'response_url': request.GET.get('response_url')
        })


def _redirect_to_auth_error(error_message, response_url):
    return redirect(
        '{}?error_message={}&response_url={}'.format(
            reverse('googleauth-auth-error'),
            error_message,
            response_url))


def _google_flow(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=settings.GOOGLE_API_SECRET_JSON,
        scopes=settings.GOOGLE_API_SCOPES)
    flow.redirect_uri = request.build_absolute_uri(reverse('googleauth-auth-redirect'))
    return flow
