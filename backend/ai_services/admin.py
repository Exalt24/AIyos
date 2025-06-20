from django.contrib import admin
from django.utils.html import format_html
from .models import AIProvider, AIModel, AIRequest, AITemplate, AIUsageQuota

@admin.register(AIProvider)
class AIProviderAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'provider_type', 'is_active', 'requests_per_minute',
        'cost_per_input_display', 'cost_per_output_display'
    ]
    list_filter = ['provider_type', 'is_active']
    search_fields = ['name']
    
    fieldsets = (
        ('Provider Information', {
            'fields': ('name', 'provider_type', 'api_endpoint', 'is_active')
        }),
        ('Cost Configuration', {
            'fields': ('cost_per_input_token', 'cost_per_output_token')
        }),
        ('Rate Limits', {
            'fields': ('requests_per_minute', 'tokens_per_minute')
        }),
    )
    
    def cost_per_input_display(self, obj):
        return f"${obj.cost_per_input_token:.6f}"
    cost_per_input_display.short_description = 'Input Cost/Token'
    
    def cost_per_output_display(self, obj):
        return f"${obj.cost_per_output_token:.6f}"
    cost_per_output_display.short_description = 'Output Cost/Token'

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'provider', 'model_type', 'capability_level',
        'min_subscription_tier', 'supports_tagalog', 'is_active'
    ]
    list_filter = [
        'provider', 'model_type', 'capability_level', 'min_subscription_tier',
        'supports_tagalog', 'supports_filipino_context', 'is_active'
    ]
    search_fields = ['name', 'model_id']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('provider', 'name', 'model_id', 'model_type', 'capability_level')
        }),
        ('Capabilities', {
            'fields': ('max_context_tokens', 'max_output_tokens', 'supports_functions', 'supports_streaming')
        }),
        ('Filipino Context', {
            'fields': ('supports_tagalog', 'supports_filipino_context')
        }),
        ('Access Control', {
            'fields': ('min_subscription_tier', 'is_active')
        }),
        ('Performance', {
            'fields': ('average_response_time_ms', 'reliability_score')
        }),
    )

@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'model', 'request_type', 'status', 'total_tokens',
        'cost_php_display', 'response_time_display', 'created_at'
    ]
    list_filter = [
        'request_type', 'status', 'model__provider', 'created_at'
    ]
    search_fields = ['user__email', 'user__company_name']
    readonly_fields = [
        'id', 'created_at', 'completed_at', 'duration_seconds'
    ]
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'model', 'request_type', 'status')
        }),
        ('Content', {
            'fields': ('input_data', 'processed_input', 'output_data'),
            'classes': ('collapse',)
        }),
        ('Usage & Cost', {
            'fields': ('input_tokens', 'output_tokens', 'total_tokens', 'cost_usd', 'cost_php')
        }),
        ('Performance', {
            'fields': ('response_time_ms', 'created_at', 'completed_at')
        }),
        ('Error Information', {
            'fields': ('error_message', 'error_code', 'retry_count'),
            'classes': ('collapse',)
        }),
        ('Context', {
            'fields': ('workflow_execution', 'user_context'),
            'classes': ('collapse',)
        }),
    )
    
    def cost_php_display(self, obj):
        return f"₱{obj.cost_php:.2f}"
    cost_php_display.short_description = 'Cost (PHP)'
    
    def response_time_display(self, obj):
        if obj.response_time_ms:
            if obj.response_time_ms > 5000:
                color = 'red'
            elif obj.response_time_ms > 2000:
                color = 'orange'
            else:
                color = 'green'
            return format_html(
                '<span style="color: {};">{} ms</span>',
                color, obj.response_time_ms
            )
        return "-"
    response_time_display.short_description = 'Response Time'

@admin.register(AITemplate)
class AITemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'business_context', 'supports_tagalog',
        'usage_count', 'success_rate_display', 'is_active', 'is_premium'
    ]
    list_filter = [
        'category', 'business_context', 'supports_tagalog',
        'is_active', 'is_premium'
    ]
    search_fields = ['name', 'tagalog_name', 'description']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'tagalog_name', 'description', 'category', 'business_context')
        }),
        ('Template Content', {
            'fields': ('system_prompt', 'user_prompt_template', 'example_input', 'example_output')
        }),
        ('Configuration', {
            'fields': ('recommended_model_type', 'max_tokens', 'temperature')
        }),
        ('Filipino Context', {
            'fields': ('supports_tagalog', 'supports_mixed_language')
        }),
        ('Access & Usage', {
            'fields': ('is_active', 'is_premium', 'usage_count', 'success_rate')
        }),
    )
    
    readonly_fields = ['usage_count', 'success_rate']
    
    def success_rate_display(self, obj):
        rate = obj.success_rate
        if rate >= 90:
            color = 'green'
        elif rate >= 70:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = 'Success Rate'

@admin.register(AIUsageQuota)
class AIUsageQuotaAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'period_type', 'period_start', 'requests_usage_display',
        'tokens_usage_display', 'cost_usage_display', 'is_exceeded'
    ]
    list_filter = ['period_type', 'is_exceeded', 'period_start']
    search_fields = ['user__email', 'user__company_name']
    
    fieldsets = (
        ('Quota Information', {
            'fields': ('user', 'period_type', 'period_start', 'period_end')
        }),
        ('Limits', {
            'fields': ('max_requests', 'max_tokens', 'max_cost_usd')
        }),
        ('Current Usage', {
            'fields': ('current_requests', 'current_tokens', 'current_cost_usd', 'is_exceeded')
        }),
    )
    
    def requests_usage_display(self, obj):
        percentage = obj.requests_percentage
        color = 'red' if percentage >= 90 else 'orange' if percentage >= 70 else 'green'
        return format_html(
            '<span style="color: {};">{}/{} ({:.1f}%)</span>',
            color, obj.current_requests, obj.max_requests, percentage
        )
    requests_usage_display.short_description = 'Requests Usage'
    
    def tokens_usage_display(self, obj):
        percentage = obj.tokens_percentage
        color = 'red' if percentage >= 90 else 'orange' if percentage >= 70 else 'green'
        return format_html(
            '<span style="color: {};">{}/{} ({:.1f}%)</span>',
            color, obj.current_tokens, obj.max_tokens, percentage
        )
    tokens_usage_display.short_description = 'Tokens Usage'
    
    def cost_usage_display(self, obj):
        percentage = obj.cost_percentage
        color = 'red' if percentage >= 90 else 'orange' if percentage >= 70 else 'green'
        return format_html(
            '<span style="color: {};">${:.2f}/${:.2f} ({:.1f}%)</span>',
            color, obj.current_cost_usd, obj.max_cost_usd, percentage
        )
    cost_usage_display.short_description = 'Cost Usage'