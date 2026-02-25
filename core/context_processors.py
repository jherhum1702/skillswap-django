def preferences(request):
    """
    Context processor that reads user theme and lenguage preferences from cookies and makes them available in all templates.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing user cookies.

    Returns
    -------
    dict: Dictionary containing user preferences for theme and language, with default values if cookies are not set.

    Example
    -------
        In template: {{ theme }} or {{ lang }}
    """
    return {
        'theme': request.COOKIES.get('theme', 'light'),
        'lang': request.COOKIES.get('lang', 'es')
    }
