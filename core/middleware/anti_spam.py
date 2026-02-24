from datetime import timedelta

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpRequest


class SpamMiddleware:
    """
    Middleware that limits how many posts a user can create within a day.

    This middleware checks how many posts the user has created in the
    last 24 hours (a day). If the user has posted more than twice in that period, an error
    message is shown and the user is redirected to the home page, preventing spam.

    Attributes:
        get_response (Callable): Django's function that calls the next middleware or view.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the response function.

        Args:
            get_response (Callable): Processes the request and returns a HttpResponse.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Check if the user has exceeded the daily posting limit only if it's a POST request to /posts/create/.

        If the user has made more than two posts in the last 24 hours, an error message is displayed
        and the user is redirected to the home page. Otherwise, the request continues.

        Args:
            request (HttpRequest): The current HTTP request object.

        Returns:
            HttpResponse: A redirect to 'core:home' if the posting limit is exceeded,
            or the normal view response if allowed.
        """
        if request.path == '/posts/create/' and request.method == 'POST':
            user = request.user
            if hasattr(user, 'publicaciones') and user.publicaciones.filter(fecha_creacion__gte=timedelta(days=1)).count() >= 2:
                messages.error(
                    request,
                    "You can't post more than two times in a day. Please try again later."
                )
                return redirect('core:home')

        response = self.get_response(request)
        return response # Returns response if the middleware detects it's not spam.