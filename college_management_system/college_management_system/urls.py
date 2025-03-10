from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='auth/login/', permanent=False)),
    path('auth/', include('authentication.urls')),
    path('core/', include('core.urls')),
    path('admin-portal/', include('admin_portal.urls')),
    path('hod-portal/', include('hod_portal.urls')),
    path('faculty-portal/', include('faculty_portal.urls')),
    path('lab-assistant-portal/', include('lab_assistant_portal.urls')),
    path('student-portal/', include('student_portal.urls')),
]