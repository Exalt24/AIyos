from django.contrib import admin
from django.utils.html import format_html
from .models import AutomationWorkflow, AutomationAction, WorkflowExecution, AutomationTemplate

@admin.register(AutomationWorkflow)
class AutomationWorkflowAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'status', 'trigger_type', 'total_executions', 
        'success_rate_display', 'last_executed', 'created_at'
    ]
    list_filter = [
        'status', 'trigger_type', 'use_ai_processing', 'business_hours_only',
        'language_context', 'created_at'
    ]
    search_fields = ['name', 'user__email', 'user__company_name', 'description']
    readonly_fields = [
        'id', 'total_executions', 'successful_executions', 'failed_executions',
        'last_executed', 'success_rate_display', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'user', 'status')
        }),
        ('Trigger Configuration', {
            'fields': ('trigger_type', 'trigger_config')
        }),
        ('AI Configuration', {
            'fields': ('use_ai_processing', 'ai_model_preference', 'ai_instructions')
        }),
        ('Filipino Business Context', {
            'fields': ('business_hours_only', 'language_context')
        }),
        ('Statistics', {
            'fields': ('total_executions', 'successful_executions', 'failed_executions', 'success_rate_display', 'last_executed'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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

class AutomationActionInline(admin.TabularInline):
    model = AutomationAction
    extra = 0
    fields = ['order', 'name', 'action_type', 'ai_enhanced', 'is_conditional']
    readonly_fields = ['created_at']

@admin.register(AutomationAction)
class AutomationActionAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'name', 'action_type', 'order', 'ai_enhanced', 'is_conditional']
    list_filter = ['action_type', 'ai_enhanced', 'is_conditional', 'retry_on_failure']
    search_fields = ['workflow__name', 'name', 'workflow__user__company_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('workflow', 'name', 'action_type', 'order')
        }),
        ('Configuration', {
            'fields': ('action_config', 'delay_seconds')
        }),
        ('Conditional Logic', {
            'fields': ('is_conditional', 'conditions')
        }),
        ('AI Enhancement', {
            'fields': ('ai_enhanced', 'ai_prompt_template')
        }),
        ('Error Handling', {
            'fields': ('retry_on_failure', 'max_retries')
        }),
    )

@admin.register(WorkflowExecution)
class WorkflowExecutionAdmin(admin.ModelAdmin):
    list_display = [
        'workflow', 'status', 'started_at', 'duration_display', 
        'ai_calls_made', 'success_percentage_display'
    ]
    list_filter = ['status', 'started_at', 'workflow__user']
    search_fields = ['workflow__name', 'workflow__user__email', 'workflow__user__company_name']
    readonly_fields = [
        'id', 'started_at', 'completed_at', 'duration_seconds',
        'success_percentage_display'
    ]
    
    fieldsets = (
        ('Execution Info', {
            'fields': ('workflow', 'status', 'started_at', 'completed_at', 'duration_seconds')
        }),
        ('Data', {
            'fields': ('trigger_data', 'output_data'),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message', 'error_details'),
            'classes': ('collapse',)
        }),
        ('AI Usage', {
            'fields': ('ai_calls_made', 'ai_tokens_used', 'ai_cost_estimate')
        }),
        ('Performance', {
            'fields': ('actions_completed', 'actions_failed', 'success_percentage_display')
        }),
        ('Execution Log', {
            'fields': ('execution_log',),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        if obj.duration_seconds:
            return f"{obj.duration_seconds:.2f}s"
        return "-"
    duration_display.short_description = 'Duration'
    
    def success_percentage_display(self, obj):
        percentage = obj.success_percentage
        if percentage >= 90:
            color = 'green'
        elif percentage >= 70:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, percentage
        )
    success_percentage_display.short_description = 'Success %'

@admin.register(AutomationTemplate)
class AutomationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'business_type', 'category', 'usage_count', 
        'rating', 'is_featured', 'is_premium'
    ]
    list_filter = [
        'business_type', 'category', 'is_featured', 'is_premium', 'created_at'
    ]
    search_fields = ['name', 'description', 'tagalog_name']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'tagalog_name', 'description', 'tagalog_description')
        }),
        ('Classification', {
            'fields': ('business_type', 'category', 'is_featured', 'is_premium')
        }),
        ('Configuration', {
            'fields': ('workflow_config', 'required_integrations', 'estimated_setup_time')
        }),
        ('Content', {
            'fields': ('setup_instructions', 'preview_image', 'demo_video_url')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'rating'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['usage_count', 'created_at', 'updated_at']