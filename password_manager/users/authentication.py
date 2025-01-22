from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class CustomTokenAuthentication(TokenAuthentication):
    """
    Custome authentication class.".
    """
    keyword = None

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth:
            return None

        if len(auth) == 1:
            # if token without prefix
            token = auth[0]
        elif len(auth) == 2:
            # if token with prefix, ignore prefix
            token = auth[1]
        else:
            raise exceptions.AuthenticationFailed('Invalid token header')

        return self.authenticate_credentials(token)

