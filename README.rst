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

1. Set default login success view name as `GOOGLEAUTH_SUCCESS_VIEW`::

    GOOGLEAUTH_SUCCESS_VIEW = 'login-success-view-name'

   If this view is not set, a simple login success page will be shown.

2. Set default login error view name as `GOOGLEAUTH_ERROR_VIEW`::

    GOOGLEAUTH_ERROR_VIEW = 'login-error-view-name'

   The `error_message` and `response_url` query string is available in the `request.GET` parameter of the view function.
   If this view is not set, a simple login success page will be shown.

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

