from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from accounts import models
from accounts import serializers


class RegisterView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(is_active=False)


class VerifyUserView(GenericAPIView):
    serializer_class = serializers.VerifyUserSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_qs = models.VerificationToken.objects.filter(user__username=request.data['username'],
                                                           token=request.data['token'],
                                                           type=models.VerificationToken.Types.ACCOUNT)

        if not token_qs.exists():
            return Response({'status': 'failed', 'message': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)

        token = token_qs.first()
        token.user.is_active = True
        token.user.save()
        token.delete()

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
