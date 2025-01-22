from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    """
    Custom authentication scheme.
    """
    target_class = 'users.authentication.CustomTokenAuthentication'
    name = 'CustomTokenAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication without the "Token" prefix.',
        }