# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Ensure this URL is correct
    path('accounts/', views.show_accounts, name='show_accounts'),  # View all accounts
    path('fund_transfer/<int:receiver_id>/', views.fund_transfer, name='fund_transfer'),
    path('loan/', views.loan_request, name='loan_request'),
]