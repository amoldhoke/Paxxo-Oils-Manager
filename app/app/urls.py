from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,)


urlpatterns = [
    # Path to admin page
    path('admin/', admin.site.urls),
    path('', include('Inbox.urls')),
    path('api/', include('Inbox.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
]

# Error handling (404 & 500 )
handler = 'Inbox.views.E_500'
handler = 'Inbox.views.E_404'
