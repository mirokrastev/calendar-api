from django.urls import path

from rest_framework_simplejwt import views as jwt_views

app_name = 'acocunts'

urlpatterns = [
    path('api/auth/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]
