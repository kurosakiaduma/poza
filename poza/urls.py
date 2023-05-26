"""poza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from chat.views import Ajax
from ajax_select import urls as ajax_select_urls
import django_pesapal

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/",include("chat.urls")),
    path("", include("booking.urls")),
    path("members", include("django.contrib.auth.urls")),
    path("members", include("members.urls")),
    path('ajax', Ajax, name='ajax'),
    path(r'^ajax_select/', include(ajax_select_urls)),
    #...
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Configuring links to serve static user-uploaded content
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#Configuring admin titles
admin.site.site_header = "Poza Specialist Clinic Admin"