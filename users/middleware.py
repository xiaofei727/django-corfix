from django.http import Http404
from django.conf import settings

class StackOverflowMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.