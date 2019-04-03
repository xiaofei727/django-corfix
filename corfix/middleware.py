from django.http import Http404
from django.conf import settings
from django.shortcuts import render, redirect

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        print(request.path)
        if (request.path != '/') and (request.path != '/signin') and (request.path != '/signin_post') and (request.path != '/signup_post') and (request.path != '/logout'):
            if "userid" in request.session:
                print('auth token success')
            else:
                print('require signin')
                return redirect('signin')
        response = self.get_response(request)
        

        # Code to be executed for each request/response after
        # the view is called.

        return response