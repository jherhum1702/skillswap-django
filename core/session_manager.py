class SessionManager:
    """
    Manager for handling user search filter sessions.

    Provides methods to save, retrieve, and clear search filters
    from the user's session during their navigation.
    """

    FILTERS_KEY = 'search_filters'

    @staticmethod
    def save_filters(request, q=None, tipo=None, estado=None):
        """
        Save search filters to the session.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object containing the session.
        q : str, optional
            Search query string.
        tipo : str, optional
            Post type filter (BUSCO or OFREZCO).
        estado : bool or str, optional
            Post status filter (active/inactive).

        Returns
        -------
        None
            Modifies the request.session directly.

        Example
        -------
        >>> SessionManager.save_filters(request, q='python', tipo='BUSCO')
        """
        filters = request.session.get(SessionManager.FILTERS_KEY, {})

        if q is not None:
            filters['q'] = q
        if tipo is not None:
            filters['tipo'] = tipo
        if estado is not None:
            filters['estado'] = estado

        request.session[SessionManager.FILTERS_KEY] = filters

    @staticmethod
    def get_filters(request):
        """
        Retrieve search filters from the session.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object containing the session.

        Returns
        -------
        dict
            Dictionary containing saved filters (q, tipo, estado).
            Returns empty dict if no filters are stored.

        Example
        -------
        >>> filters = SessionManager.get_filters(request)
        >>> filters.get('q')  # Get search query
        'python'
        """
        return request.session.get(SessionManager.FILTERS_KEY, {})

    @staticmethod
    def clear_filters(request):
        """
        Clear all search filters from the session.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object containing the session.

        Returns
        -------
        None
            Modifies the request.session directly.

        Example
        -------
        >>> SessionManager.clear_filters(request)
        """
        if SessionManager.FILTERS_KEY in request.session:
            del request.session[SessionManager.FILTERS_KEY]

