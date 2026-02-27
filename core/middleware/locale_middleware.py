from django.utils.translation import activate
from django.conf import settings


class LocaleFromCookieMiddleware:
    """
    Middleware to set the language based on a cookie.

    If the cookie contains 'en' or 'es', Django will use that language.
    If there is no cookie, it will use LANGUAGE_CODE from settings.py, which is 'es' in this case.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.COOKIES.get('lang', 'es')

        # Extract language codes from LANGUAGES setting (which is a list of tuples)
        valid_langs = [code for code, name in settings.LANGUAGES]

        if lang in valid_langs:
            activate(lang)

        response = self.get_response(request)
        return response