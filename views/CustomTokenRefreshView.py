from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.exceptions import InvalidToken
from typing import Any

# Constants for cookie names and max age values
ACCESS_TOKEN_COOKIE_NAME = 'accessToken'
REFRESH_TOKEN_COOKIE_NAME = 'refreshToken'
ACCESS_TOKEN_MAX_AGE = 3600  # 1 hour
REFRESH_TOKEN_MAX_AGE = 3600 * 24  # 1 day

# Custom view to refresh JWT tokens using a refresh token stored in cookies
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to handle JWT token refresh using a refresh token stored in cookies.
    This view extends the TokenRefreshView from the djangorestframework-simplejwt package.
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests to refresh JWT tokens.

        Args:
            request (Request): The HTTP request object.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Response: The HTTP response object containing the new access token in cookies.
        """
        # Retrieve the refresh token from cookies
        refresh_token: str = request.COOKIES.get(REFRESH_TOKEN_COOKIE_NAME)
        if not refresh_token:
            # Return an error response if the refresh token is missing
            return Response({'detail': 'Refresh token missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the serializer with the refresh token
        serializer: Serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            # Validate the serializer data
            serializer.is_valid(raise_exception=True)
        except InvalidToken as e:
            # Return an error response if validation fails
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create a response with the validated data
        response: Response = Response(serializer.validated_data)
        # Retrieve the new access token from the validated data
        access: str = serializer.validated_data.get('access')

        # Set the new access token in cookies
        response.set_cookie(
            ACCESS_TOKEN_COOKIE_NAME, 
            access, 
            httponly=True, 
            secure=True,  
            samesite='None',
            max_age=ACCESS_TOKEN_MAX_AGE,  # 1 hour
        )

        # Remove the refresh and access tokens from the response data
        response.data.pop('refresh', None)
        response.data.pop('access', None)

        # Return the response
        return response