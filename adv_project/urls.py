from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from rest_framework import routers
from rest_framework.authtoken import views


from adventure.api import RoomViewSet


router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('api/', include(router.urls)),
]
