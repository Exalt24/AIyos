from django.contrib import admin
from django.utils.html import format_html
from .models import Integration, IntegrationLog, WebhookEndpoint

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'service_name', 'integration_type', 
        'health_status_display', 'is_active', 'success_rate_display', 'last_used'
    ]
    list_filter = [
        'integration_type', 'health_status', 'is_active', 'service_name', 'created_at'
    ]
    search_fields = ['name', 'service_name', 'user__email', 'user__company_name']
    readonly_fields = [
        'id', 'total_requests', 'successful_requests', 'failed_requests',
        'last_health_check', 'last_used', 'success_rate_display', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Integration Details', {
            'fields': ('user', 'name', 'integration_type', 'service_name', 'service_url', 'is_active')
        }),
        ('Configuration', {
            'fields': ('config_data',)
        }),
        ('Authentication', {
            'fields': ('api_key', 'api_secret', 'access_token', 'refresh_token', 'webhook_secret'),
            'classes': ('collapse',)
        }),
        ('OAuth', {
            'fields': ('oauth_provider', 'oauth_scope', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('Health & Monitoring', {
            'fields': ('health_status', 'health_message', 'last_health_check')
        }),
        ('Usage Statistics', {
            'fields': ('total_requests', 'successful_requests', 'failed_requests', 'success_rate_display', 'last_used'),
            'classes': ('collapse',)
        }),
        ('Rate Limiting', {
            'fields': ('rate_limit_remaining', 'rate_limit_reset'),
            'classes': ('collapse',)
        }),
    )
    
    def health_status_display(self, obj):
        colors = {
            'healthy': 'green',
            'warning': 'orange',
            'error': 'red',
            'disconnected': 'gray'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.health_status, 'black'),
            obj.get_health_status_display()
        )
    health_status_display.short_description = 'Health Status'
    
    def success_rate_display(self, obj):
        rate = obj.success_rate
        if rate >= 95:
            color = 'green'
        elif rate >= 80:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = 'Success Rate'

@admin.register(IntegrationLog)
class IntegrationLogAdmin(admin.ModelAdmin):
    list_display = [
        'integration', 'log_type', 'method', 'status_code', 
        'response_time_display', 'created_at'
    ]
    list_filter = ['log_type', 'status_code', 'created_at', 'integration__service_name']
    search_fields = ['integration__name', 'endpoint', 'error_message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Log Information', {
            'fields': ('integration', 'log_type', 'method', 'endpoint', 'status_code')
        }),
        ('Request/Response', {
            'fields': ('request_data', 'response_data'),
            'classes': ('collapse',)
        }),
        ('Error Details', {
            'fields': ('error_message', 'error_code'),
            'classes': ('collapse',)
        }),
        ('Performance & Context', {
            'fields': ('response_time_ms', 'workflow_execution', 'user_agent', 'ip_address')
        }),
    )
    
    def response_time_display(self, obj):
        if obj.response_time_ms:
            if obj.response_time_ms > 5000:  # > 5 seconds
                color = 'red'
            elif obj.response_time_ms > 2000:  # > 2 seconds
                color = 'orange'
            else:
                color = 'green'
            return format_html(
                '<span style="color: {};">{} ms</span>',
                color, obj.response_time_ms
            )
        return "-"
    response_time_display.short_description = 'Response Time'

@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'integration', 'url_path', 'status', 
        'total_requests', 'success_rate_display', 'last_triggered'
    ]
    list_filter = ['status', 'require_signature', 'auto_trigger_workflows', 'created_at']
    search_fields = ['name', 'url_path', 'integration__name']
    readonly_fields = [
        'total_requests', 'successful_requests', 'failed_requests',
        'last_triggered', 'full_url', 'success_rate_display'
    ]
    
    fieldsets = (
        ('Webhook Configuration', {
            'fields': ('integration', 'name', 'url_path', 'full_url', 'status')
        }),
        ('Security', {
            'fields': ('secret_key', 'allowed_ips', 'require_signature', 'signature_header')
        }),
        ('Processing', {
            'fields': ('auto_trigger_workflows',)
        }),
        ('Statistics', {
            'fields': ('total_requests', 'successful_requests', 'failed_requests', 'success_rate_display', 'last_triggered'),
            'classes': ('collapse',)
        }),
    )
    
    def success_rate_display(self, obj):
        rate = obj.success_rate
        if rate >= 95:
            color = 'green'
        elif rate >= 80:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = 'Success Rate'