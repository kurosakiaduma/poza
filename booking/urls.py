from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500


handler500 = views.custom_error_handler

urlpatterns = [
    path('', views.index, name='index'),
    path('bookings', views.booking, name='booking'),
    path('uploads',views.userPanel, name='userPanel'),
    path('user-panel/<slug:foo>', views.userPanel, name='userPanel'),
    path('user-update/<int:app_id>', views.userUpdate, name='userUpdate'),
    path('staff-panel/<slug:foo>', views.staffPanel, name='staffPanel'),
    path('staff-panel/<slug:app_id>', views.staffPanel, name='staffPanel'),
    path('staff-panel/', views.staffPanel, name='staffPanel'),
    path('analytics/', views.analytics, name='analytics'),
    path('doctors/', views.doctors, name='doctors'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)