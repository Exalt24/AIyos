from rest_framework import serializers
from .models import AutomationWorkflow, AutomationAction, WorkflowExecution, AutomationTemplate

class AutomationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationAction
        fields = [
            'id', 'name', 'action_type', 'action_config', 'order',
            'conditions', 'is_conditional', 'ai_enhanced', 'ai_prompt_template',
            'retry_on_failure', 'max_retries', 'delay_seconds',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AutomationWorkflowListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing workflows"""
    actions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AutomationWorkflow
        fields = [
            'id', 'name', 'description', 'status', 'trigger_type',
            'total_executions', 'success_rate', 'last_executed',
            'actions_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_executions', 'success_rate', 'last_executed',
            'actions_count', 'created_at', 'updated_at'
        ]
    
    def get_actions_count(self, obj):
        return obj.actions.count()

class AutomationWorkflowDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with nested actions"""
    actions = AutomationActionSerializer(many=True, read_only=True)
    
    class Meta:
        model = AutomationWorkflow
        fields = [
            'id', 'name', 'description', 'status', 'trigger_type', 'trigger_config',
            'ai_instructions', 'use_ai_processing', 'ai_model_preference',
            'business_hours_only', 'language_context',
            'total_executions', 'successful_executions', 'failed_executions',
            'success_rate', 'last_executed', 'actions',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_executions', 'successful_executions', 'failed_executions',
            'success_rate', 'last_executed', 'created_at', 'updated_at'
        ]

class AutomationWorkflowCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workflows"""
    
    class Meta:
        model = AutomationWorkflow
        fields = [
            'name', 'description', 'trigger_type', 'trigger_config',
            'ai_instructions', 'use_ai_processing', 'ai_model_preference',
            'business_hours_only', 'language_context'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class WorkflowExecutionSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    
    class Meta:
        model = WorkflowExecution
        fields = [
            'id', 'workflow', 'workflow_name', 'status', 'trigger_data',
            'execution_log', 'output_data', 'error_message', 'error_details',
            'started_at', 'completed_at', 'duration_seconds',
            'ai_calls_made', 'ai_tokens_used', 'ai_cost_estimate',
            'actions_completed', 'actions_failed', 'success_percentage'
        ]
        read_only_fields = [
            'id', 'workflow_name', 'started_at', 'completed_at', 'duration_seconds',
            'success_percentage'
        ]

class AutomationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationTemplate
        fields = [
            'id', 'name', 'tagalog_name', 'description', 'tagalog_description',
            'business_type', 'category', 'workflow_config', 'required_integrations',
            'estimated_setup_time', 'setup_instructions', 'preview_image',
            'demo_video_url', 'usage_count', 'rating', 'is_featured', 'is_premium'
        ]
        read_only_fields = ['id', 'usage_count', 'rating']

class CreateWorkflowFromTemplateSerializer(serializers.Serializer):
    """Serializer for creating workflow from template"""
    template_id = serializers.UUIDField()
    workflow_name = serializers.CharField(max_length=255)
    customizations = serializers.JSONField(default=dict, required=False)
    
    def validate_template_id(self, value):
        try:
            template = AutomationTemplate.objects.get(id=value)
            # Check if user's subscription allows premium templates
            user = self.context['request'].user
            if template.is_premium and user.subscription_tier == 'starter':
                raise serializers.ValidationError(
                    "Premium templates require Business or Pro subscription"
                )
            return value
        except AutomationTemplate.DoesNotExist:
            raise serializers.ValidationError("Template not found")