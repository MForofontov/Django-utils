import gzip
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class ResponseCompressionMiddleware(MiddlewareMixin):
    """
    Middleware to compress HTTP responses using gzip.
    
    This middleware compresses the content of HTTP responses with 'text/html' content type
    using gzip to reduce the size of the response.
    """
    
    def process_response(self, request, response):
        """
        Compress the response content if the content type is 'text/html'.
        
        Parameters
        ----------
        request : HttpRequest
            The incoming HTTP request.
        response : HttpResponse
            The HTTP response to be processed.
        
        Returns
        -------
        HttpResponse
            The processed HTTP response with compressed content if applicable.
        """
        # Check if the response content type is 'text/html'
        if response['Content-Type'] == 'text/html':
            # Compress the response content using gzip
            response.content = gzip.compress(response.content)
            # Set the 'Content-Encoding' header to 'gzip'
            response['Content-Encoding'] = 'gzip'
            # Update the 'Content-Length' header with the length of the compressed content
            response['Content-Length'] = str(len(response.content))
        return response