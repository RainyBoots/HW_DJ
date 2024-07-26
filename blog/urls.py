from django.contrib import admin
from django.urls import path, include
from python_blog import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name="main"),
    path('blog/', include('python_blog.urls')),
    path('about/', views.about, name="about"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
