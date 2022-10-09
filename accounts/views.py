from rest_framework.generics import CreateAPIView

from accounts import models
from accounts import serializers


class RegisterView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()
