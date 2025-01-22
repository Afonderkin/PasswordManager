from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountSerializer, DecryptPasswordSerializer
from .models import Accounts


class AccountsListCreateView(generics.ListCreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


class DecryptPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=DecryptPasswordSerializer,
        responses={
            200: DecryptPasswordSerializer,
            400: "Bad request",
            404: "Account not found"
        }
    )
    def post(self, request, pk):
        try:
            account = Accounts.objects.get(pk=pk, user=request.user)
        except Accounts.DoesNotExist:
            raise NotFound("Account not found or you do not have permission to access it.")

        serializer = DecryptPasswordSerializer(data=request.data)
        if serializer.is_valid():
            master_password = serializer.validated_data['master_password']
            try:
                decrypted_password = account.get_password(master_password)
                return Response(
                    {"decrypted_password": decrypted_password},
                    status=status.HTTP_200_OK
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)