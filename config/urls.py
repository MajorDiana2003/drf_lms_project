
from django.contrib import admin
from django.urls import path, include
from lms.views import api_view, api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),

    # Подключаем API
    path('api/', include('lms.urls', namespace='lms')),
    path('api/users/', include('users.urls', namespace='users')),
]
