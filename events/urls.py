from django.urls import path, include
from rest_framework import routers

from events import views

app_name = 'events'

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('events', views.EventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
