from django.urls import path
from . import views

urlpatterns = [
    # AI Models
    path('models/', views.AIModelListView.as_view(), name='ai-model-list'),
    
    # AI Requests
    path('requests/', views.AIRequestListView.as_view(), name='ai-request-list'),
    path('requests/<uuid:pk>/', views.AIRequestDetailView.as_view(), name='ai-request-detail'),
    
    # Core AI Features
    path('email-to-task/', views.email_to_task, name='email-to-task'),
    path('generate-content/', views.generate_social_content, name='generate-social-content'),
    path('analyze-text/', views.analyze_text, name='analyze-text'),
    path('custom-request/', views.custom_ai_request, name='custom-ai-request'),
    
    # Templates
    path('templates/', views.AITemplateListView.as_view(), name='ai-template-list'),
    path('templates/<int:pk>/', views.AITemplateDetailView.as_view(), name='ai-template-detail'),
    
    # Usage & Monitoring
    path('usage-stats/', views.ai_usage_stats, name='ai-usage-stats'),
    path('quota-status/', views.ai_quota_status, name='ai-quota-status'),
    path('health-check/', views.ai_health_check, name='ai-health-check'),
    
    # Utility
    path('request-types/', views.ai_request_types, name='ai-request-types'),
]