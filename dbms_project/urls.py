from django.contrib import admin
from django.urls import path, include  # include needed for including app URLs
from login_page import views  # Import views from the 'login_page' app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Root login view
    path('login-page/', include('login_page.urls')),  # Include the 'login_page' URLs here
]
