from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from accounts import models
from accounts import serializers
from accounts import schemas


class RegisterView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()
    swagger_schema = schemas.RegisterSchema

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(is_active=False)


class VerifyUserView(GenericAPIView):
    """
    Takes a username and a token and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    queryset = models.VerificationToken.objects.filter(type=models.VerificationToken.Types.ACCOUNT)
    serializer_class = serializers.VerifyUserSerializer
    permission_classes = ()
    swagger_schema = schemas.VerifyUserSchema

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
        data = {'refresh': str(jwt_token),
                'access': str(jwt_token.access_token)}

        return Response(TokenRefreshSerializer(data).data, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_kwargs = {'user__username': self.request.data['username'],
                         'token': self.request.data['token']}

        token = get_object_or_404(queryset, **lookup_kwargs)
        return token
