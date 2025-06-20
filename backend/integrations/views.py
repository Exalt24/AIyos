from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Integration, IntegrationLog, WebhookEndpoint
from .serializers import (
    IntegrationListSerializer, IntegrationDetailSerializer,
    IntegrationCreateSerializer, IntegrationLogSerializer,
    WebhookEndpointSerializer, TestIntegrationSerializer
)

class IntegrationListView(generics.ListCreateAPIView):
    """List user's integrations or create new one"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['integration_type', 'health_status', 'is_active']
    search_fields = ['name', 'service_name']
    ordering_fields = ['created_at', 'name', 'last_used']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Integration.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IntegrationCreateSerializer
        return IntegrationListSerializer

class IntegrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete specific integration"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IntegrationDetailSerializer
    
    def get_queryset(self):
        return Integration.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_integration(request, integration_id):
    """Test integration connectivity"""
    integration = get_object_or_404(
        Integration, 
        id=integration_id, 
        user=request.user
    )
    
    serializer = TestIntegrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    test_type = serializer.validated_data['test_type']
    test_data = serializer.validated_data.get('test_data', {})
    
    # TODO: Implement actual integration testing logic
    # This would call the actual service APIs to test connectivity
    
    # For now, return mock response
    result = {
        'success': True,
        'message': f'{test_type} completed successfully',
        'test_type': test_type,
        'response_time': 150,  # milliseconds
        'details': {
            'integration': integration.name,
            'service': integration.service_name,
            'health_status': 'healthy'
        }
    }
    
    # Log the test
    IntegrationLog.objects.create(
        integration=integration,
        log_type='health_check',
        method='POST',
        endpoint=f'/test/{test_type}',
        status_code=200,
        response_time_ms=150,
        request_data=test_data,
        response_data=result
    )
    
    return Response(result)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def refresh_integration_auth(request, integration_id):
    """Refresh integration authentication tokens"""
    integration = get_object_or_404(
        Integration, 
        id=integration_id, 
        user=request.user
    )
    
    if not integration.refresh_token:
        return Response(
            {'error': 'No refresh token available'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # TODO: Implement actual token refresh logic for each service
    # This would call the OAuth refresh endpoint for the service
    
    return Response({
        'message': 'Authentication refreshed successfully',
        'expires_at': None  # Would be actual expiration time
    })

class IntegrationLogListView(generics.ListAPIView):
    """List integration logs"""
    serializer_class = IntegrationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['log_type', 'status_code', 'integration']
    ordering_fields = ['created_at', 'response_time_ms']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return IntegrationLog.objects.filter(
            integration__user=self.request.user
        ).select_related('integration')

class WebhookEndpointListView(generics.ListCreateAPIView):
    """List and create webhook endpoints"""
    serializer_class = WebhookEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'integration']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return WebhookEndpoint.objects.filter(
            integration__user=self.request.user
        ).select_related('integration')
    
    def perform_create(self, serializer):
        # Auto-generate URL path if not provided
        import uuid
        if not serializer.validated_data.get('url_path'):
            serializer.validated_data['url_path'] = str(uuid.uuid4())
        
        # Auto-generate secret key if not provided
        if not serializer.validated_data.get('secret_key'):
            serializer.validated_data['secret_key'] = str(uuid.uuid4())
        
        serializer.save()

class WebhookEndpointDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete webhook endpoint"""
    serializer_class = WebhookEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WebhookEndpoint.objects.filter(
            integration__user=self.request.user
        ).select_related('integration')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_integrations(request):
    """Get list of available integration types"""
    integrations = [
        {
            'type': 'gcash',
            'name': 'GCash',
            'description': 'Philippine mobile payment service',
            'category': 'payment',
            'logo': '/static/images/integrations/gcash.png',
            'setup_difficulty': 'easy',
            'popular': True
        },
        {
            'type': 'paymaya',
            'name': 'PayMaya',
            'description': 'Philippine digital payment platform',
            'category': 'payment',
            'logo': '/static/images/integrations/paymaya.png',
            'setup_difficulty': 'easy',
            'popular': True
        },
        {
            'type': 'shopee',
            'name': 'Shopee',
            'description': 'E-commerce platform integration',
            'category': 'ecommerce',
            'logo': '/static/images/integrations/shopee.png',
            'setup_difficulty': 'medium',
            'popular': True
        },
        {
            'type': 'facebook',
            'name': 'Facebook Business',
            'description': 'Social media management and ads',
            'category': 'social_media',
            'logo': '/static/images/integrations/facebook.png',
            'setup_difficulty': 'medium',
            'popular': True
        },
        {
            'type': 'bir',
            'name': 'Bureau of Internal Revenue',
            'description': 'Tax compliance and filing',
            'category': 'government',
            'logo': '/static/images/integrations/bir.png',
            'setup_difficulty': 'hard',
            'popular': False
        },
        # Add more as needed
    ]
    
    return Response(integrations)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def integration_stats(request):
    """Get integration statistics for user"""
    user = request.user
    
    integrations = Integration.objects.filter(user=user)
    logs = IntegrationLog.objects.filter(integration__user=user)
    webhooks = WebhookEndpoint.objects.filter(integration__user=user)
    
    # Calculate stats
    total_integrations = integrations.count()
    active_integrations = integrations.filter(is_active=True, health_status='healthy').count()
    total_requests = sum(integration.total_requests for integration in integrations)
    
    # Recent activity
    recent_logs = logs.order_by('-created_at')[:20]
    
    stats = {
        'integrations': {
            'total': total_integrations,
            'active': active_integrations,
            'inactive': integrations.filter(is_active=False).count(),
            'errors': integrations.filter(health_status='error').count(),
        },
        'requests': {
            'total': total_requests,
            'successful': sum(integration.successful_requests for integration in integrations),
            'failed': sum(integration.failed_requests for integration in integrations),
        },
        'webhooks': {
            'total': webhooks.count(),
            'active': webhooks.filter(status='active').count(),
        },
        'recent_activity': IntegrationLogSerializer(recent_logs, many=True).data
    }
    
    return Response(stats)