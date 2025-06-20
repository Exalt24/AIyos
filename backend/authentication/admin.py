from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BusinessProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'company_name', 'subscription_tier', 'monthly_ai_calls']
    list_filter = ['subscription_tier', 'business_type']
    search_fields = ['email', 'company_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Business', {'fields': ('company_name', 'business_type', 'subscription_tier')}),
        ('AI Usage', {'fields': ('monthly_ai_calls',)}),
    )

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'industry', 'employee_count', 'city']
    list_filter = ['industry', 'employee_count']