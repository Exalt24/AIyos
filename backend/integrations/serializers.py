from rest_framework import serializers
from .models import Integration, IntegrationLog, WebhookEndpoint

class IntegrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing integrations"""
    
    class Meta:
        model = Integration
        fields = [
            'id', 'name', 'integration_type', 'service_name', 'is_active',
            'health_status', 'success_rate', 'last_used', 'created_at'
        ]
        read_only_fields = ['id', 'success_rate', 'last_used', 'created_at']

class IntegrationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for integration management"""
    
    class Meta:
        model = Integration
        fields = [
            'id', 'name', 'integration_type', 'service_name', 'service_url',
            'config_data', 'is_active', 'health_status', 'health_message',
            'total_requests', 'successful_requests', 'failed_requests', 'success_rate',
            'last_health_check', 'last_used', 'rate_limit_remaining', 'rate_limit_reset',
            'needs_reauthorization', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_requests', 'successful_requests', 'failed_requests',
            'success_rate', 'last_health_check', 'last_used', 'health_status',
            'health_message', 'rate_limit_remaining', 'rate_limit_reset',
            'needs_reauthorization', 'created_at', 'updated_at'
        ]

class IntegrationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating integrations"""
    
    class Meta:
        model = Integration
        fields = [
            'name', 'integration_type', 'service_name', 'service_url',
            'config_data', 'api_key', 'api_secret', 'webhook_secret'
        ]
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
            'webhook_secret': {'write_only': True},
        }
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class IntegrationLogSerializer(serializers.ModelSerializer):
    integration_name = serializers.CharField(source='integration.name', read_only=True)
    
    class Meta:
        model = IntegrationLog
        fields = [
            'id', 'integration', 'integration_name', 'log_type', 'method', 'endpoint',
            'status_code', 'error_message', 'error_code', 'response_time_ms',
            'workflow_execution', 'created_at'
        ]
        read_only_fields = ['id', 'integration_name', 'created_at']

class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = [
            'id', 'integration', 'name', 'url_path', 'full_url', 'secret_key',
            'allowed_ips', 'require_signature', 'signature_header', 'status',
            'auto_trigger_workflows', 'total_requests', 'successful_requests',
            'failed_requests', 'success_rate', 'last_triggered', 'created_at'
        ]
        read_only_fields = [
            'id', 'full_url', 'total_requests', 'successful_requests',
            'failed_requests', 'success_rate', 'last_triggered', 'created_at'
        ]

class TestIntegrationSerializer(serializers.Serializer):
    """Serializer for testing integration connectivity"""
    test_type = serializers.ChoiceField(choices=[
        ('health_check', 'Health Check'),
        ('auth_test', 'Authentication Test'),
        ('api_call', 'Sample API Call'),
    ])
    test_data = serializers.JSONField(default=dict, required=False)