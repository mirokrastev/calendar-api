from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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
    queryset = models.VerificationToken.objects.filter(type=models.VerificationToken.Types.ACCOUNT)
    serializer_class = serializers.VerifyUserSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.get_object()
        user = token.user

        user.is_active = True
        user.save()
        token.delete()

        # Generate JWT Token
        jwt_token = RefreshToken.for_user(user)
        refresh = str(jwt_token)
        access = str(jwt_token.access_token)

        return Response({'refresh': refresh, 'access': access}, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_kwargs = {'user__username': self.request.data['username'],
                         'token': self.request.data['token']}

        token = get_object_or_404(queryset, **lookup_kwargs)
        return token
