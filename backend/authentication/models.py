from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended User model for AIyos with Filipino business focus"""
    
    SUBSCRIPTION_CHOICES = [
        ('starter', 'Starter - ₱1,500/month'),
        ('business', 'Business - ₱4,200/month'),
        ('pro', 'Pro - ₱8,400/month'),
    ]
    
    # Core fields
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    
    # Subscription & AI usage
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='starter')
    monthly_ai_calls = models.IntegerField(default=0)
    ai_calls_reset_date = models.DateTimeField(auto_now_add=True)
    
    # Business context
    business_type = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(
        max_length=10, 
        choices=[('en', 'English'), ('tl', 'Tagalog')], 
        default='en'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.company_name})"
    
    @property
    def ai_usage_limit(self):
        limits = {'starter': 1000, 'business': 5000, 'pro': 99999}
        return limits.get(self.subscription_tier, 1000)
    
    def can_use_ai(self):
        return self.monthly_ai_calls < self.ai_usage_limit

class BusinessProfile(models.Model):
    """Detailed business profile for AI context"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    
    # Business details
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.CharField(
        max_length=20,
        choices=[('1-5', '1-5'), ('6-20', '6-20'), ('21-50', '21-50'), ('51+', '51+')],
        blank=True
    )
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Business hours (for automation timing)
    business_start_time = models.TimeField(default='09:00')
    business_end_time = models.TimeField(default='18:00')
    
    # AI context
    business_description = models.TextField(blank=True)
    automation_goals = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.user.company_name}"