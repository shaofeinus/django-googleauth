==========
Googleauth
==========

Googleauth allows users to log in using their google account.
As a result, the default authentication system of django is overridden and can no longer be used.

Configurations
--------------

Configurations need to be set for the following files in your project.

settings.py
^^^^^^^^^^^

**Required:**

1. Add `googleauth` to `INSTALLED_APPS`::

    INSTALLED_APPS = [
        ...
        'googleauth',
    ]

2. Set `googleauth.backends.GoogleAuthBackend` as `AUTHENTICATION_BACKENDS`::
    
     AUTHENTICATION_BACKENDS = ['googleauth.backends.GoogleAuthBackend']

3. Set `googleauth-auth` as `LOGIN_URL`::

    LOGIN_URL = 'googleauth-auth'

4. Set path of google API client secret as `GOOGLE_API_SECRET_JSON`::

    GOOGLE_API_SECRET_JSON = 'path/to/client_secret.json'

   Click `here <https://developers.google.com/identity/protocols/OAuth2#basicsteps>`_ to learn more about how to generate
   the client secret file.

5. Add 'email' to 'GOOGLE_API_SCOPES' to access basic google user information::
   
    GOOGLE_API_SCOPES = [
        'email',
        ...
    ]
   
   This list can be extended by other google API access applications.

**Optional:**

1. Set default login success template as `GOOGLEAUTH_AUTH_SUCCESS_TEMPLATE`::

    GOOGLEAUTH_AUTH_SUCCESS_TEMPLATE = 'app/login_success_template.html'

   No context variables are available to be used in the template.
   If this template is not set, a default login success page will be shown (googleauth/auth_success.html).

2. Set default login error template as `GOOGLEAUTH_AUTH_ERROR_TEMPLATE`::

    GOOGLEAUTH_AUTH_ERROR_TEMPLATE = 'app/login_error_template.html'

   The `error_message` and `response_url` context variables are available to be used in the template.
   If this template is not set, a simple login error page will be shown (googleauth/auth_error.html).


urls.py
^^^^^^^

Add googleauth URLconf to `urlpatterns`::

    urlpatterns = [
        ...
        path('googleauth/', include('googleauth.urls')),
    ]



Usage
-----

Login
^^^^^

Add the django provided `@login_required` decorator to views that required authentication.
If user is not logged in, the view is redirected to the googleauth authentication framework.
Upon successful login, view is redirected back to the original view.

Manual login
""""""""""""

For manual login, call the `googleauth-auth` endpoint.
Set the `next` query string to the redirection URL after successful login.
For example::

    def manual_login(request):
        ...
        return redirect('{}?next={}'.format(reverse('googleauth-auth'), 'redirect/url/'))



Logout
^^^^^^
Call the django provided `django.contrib.auth.logout` method.
For example::

    from django.contrib.auth import logout as auth_logout

    def logout(request):
        ...
        auth_logout(request)
        ...

