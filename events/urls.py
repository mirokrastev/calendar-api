from django.urls import path, re_path, include
from rest_framework import routers

from events import views

app_name = 'events'

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    re_path('^api/', include(router.urls)),
]
