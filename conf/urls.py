from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.restapi.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.restapi.urls', namespace='restapi')),
]


# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title='DebtBook API',
        default_version='v 0.0.1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
    patterns=[
        path('api/v1/', include(api_urlpatterns))
    ]
)
urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
