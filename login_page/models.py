# login_page/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Add any other custom fields here
