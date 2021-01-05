import time
from django.http.response import HttpResponse
from contest.models import Contest

class ContestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        current_time = time.time()
        contest = Contest.objects.first()
        if current_time < contest.start_time or current_time > contest.end_time:
            return HttpResponse(content='{"detail":"Not in Contest Time"}',content_type='application/json',status=403)
        response = self.get_response(request)
        

        # Code to be executed for each request/response after
        # the view is called.
        return response

