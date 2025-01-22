from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.serializers import CustomUserSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string'},
                        'password': {'type': 'string'},
                    },
                    'required': ['username', 'password'],
                }
            }
        },
        responses={
            201: OpenApiResponse(
                description='Successful register',
                response={
                    'type': 'object',
                    'properties': {
                        'token': {'type': 'string'},
                    },
                },
            ),
            400: OpenApiResponse(
                description='Bad request',
                response={
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                    },
                },
            ),
        },
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'username': 'your_username',
                    'password': 'your_password',
                },
            ),
        ],
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string'},
                        'password': {'type': 'string'},
                    },
                    'required': ['username', 'password'],
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description='Successful login',
                response={
                    'type': 'object',
                    'properties': {
                        'token': {'type': 'string'},
                    },
                },
            ),
            400: OpenApiResponse(
                description='Bad request',
                response={
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                    },
                },
            ),
        },
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'username': 'your_username',
                    'password': 'your_password',
                },
            ),
        ],
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Logout user",
        description="Logs out the currently authenticated user by deleting their authentication token.",
        responses={
            200: OpenApiResponse(
                description="Successfully logged out.",
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "Successfully logged out."},
                    },
                },
            ),
            401: OpenApiResponse(
                description="Unauthorized",
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                    },
                },
            ),
        },
    )
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No token found for this user."}, status=status.HTTP_400_BAD_REQUEST)
