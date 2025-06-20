from django.urls import path
from . import views

urlpatterns = [
    # Integrations
    path('', views.IntegrationListView.as_view(), name='integration-list'),
    path('<uuid:pk>/', views.IntegrationDetailView.as_view(), name='integration-detail'),
    path('<uuid:integration_id>/test/', views.test_integration, name='integration-test'),
    path('<uuid:integration_id>/refresh-auth/', views.refresh_integration_auth, name='integration-refresh-auth'),
    
    # Integration Logs
    path('logs/', views.IntegrationLogListView.as_view(), name='integration-log-list'),
    
    # Webhooks
    path('webhooks/', views.WebhookEndpointListView.as_view(), name='webhook-list'),
    path('webhooks/<int:pk>/', views.WebhookEndpointDetailView.as_view(), name='webhook-detail'),
    
    # Utility endpoints
    path('available/', views.available_integrations, name='available-integrations'),
    path('stats/', views.integration_stats, name='integration-stats'),
]