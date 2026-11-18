from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='polls:index', permanent=False)),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

# Tutorial Part 8: expose the toolbar only when opted in for local development.
from django.conf import settings
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
