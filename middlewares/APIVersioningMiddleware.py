class APIVersioningMiddleware:
    """
    Middleware to handle API versioning based on request headers.
    
    This middleware extracts the API version from the 'HTTP_API_VERSION' header
    and attaches it to the request object. If the header is not present, it defaults to 'v1'.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the given get_response callable.
        
        Parameters
        ----------
        get_response : callable
            The next middleware or view in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Handle the incoming request and attach the API version to the request object.
        
        Parameters
        ----------
        request : HttpRequest
            The incoming HTTP request.
        
        Returns
        -------
        HttpResponse
            The HTTP response from the next middleware or view.
        """
        # Extract the API version from the 'HTTP_API_VERSION' header, default to 'v1' if not present
        version = request.META.get('HTTP_API_VERSION', 'v1')
        # Attach the version to the request object
        request.version = version
        # Get the response from the next middleware or view
        response = self.get_response(request)
        return response