from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('bookings', views.booking, name='booking'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('uploads',views.userPanel, name='userPanel'),
    path('user-panel/<slug:foo>', views.userPanel, name='userPanel'),
    path('user-update/<int:app_id>', views.userUpdate, name='userUpdate'),
    path('staff-panel/<slug:foo>', views.staffPanel, name='staffPanel'),
    path('staff-panel/<slug:app_id>', views.staffPanel, name='staffPanel'),
    path('staff-panel/', views.staffPanel, name='staffPanel'),
    path('analytics/', views.analytics, name='analytics'),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)