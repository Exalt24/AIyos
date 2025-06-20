from rest_framework import serializers
from .models import AIProvider, AIModel, AIRequest, AITemplate, AIUsageQuota
from .services import get_ai_service

class AIModelSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    cost_estimate = serializers.DecimalField(
        source='cost_per_request_estimate', 
        max_digits=10, 
        decimal_places=6, 
        read_only=True
    )
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'model_id', 'model_type', 'capability_level',
            'provider_name', 'max_context_tokens', 'max_output_tokens',
            'supports_tagalog', 'supports_filipino_context',
            'min_subscription_tier', 'cost_estimate', 'average_response_time_ms'
        ]

class AIRequestSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    duration_seconds = serializers.FloatField(read_only=True)
    
    class Meta:
        model = AIRequest
        fields = [
            'id', 'model', 'model_name', 'request_type', 'status',
            'input_tokens', 'output_tokens', 'total_tokens',
            'cost_usd', 'cost_php', 'response_time_ms', 'duration_seconds',
            'error_message', 'created_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'model_name', 'duration_seconds', 'created_at', 'completed_at'
        ]

class AITemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AITemplate
        fields = [
            'id', 'name', 'tagalog_name', 'description', 'category',
            'business_context', 'recommended_model_type', 'max_tokens',
            'temperature', 'supports_tagalog', 'supports_mixed_language',
            'usage_count', 'success_rate', 'is_premium', 'example_input',
            'example_output'
        ]
        read_only_fields = ['id', 'usage_count', 'success_rate']

class AIUsageQuotaSerializer(serializers.ModelSerializer):
    requests_percentage = serializers.FloatField(read_only=True)
    tokens_percentage = serializers.FloatField(read_only=True)
    cost_percentage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = AIUsageQuota
        fields = [
            'id', 'period_type', 'period_start', 'period_end',
            'max_requests', 'max_tokens', 'max_cost_usd',
            'current_requests', 'current_tokens', 'current_cost_usd',
            'requests_percentage', 'tokens_percentage', 'cost_percentage',
            'is_exceeded'
        ]
        read_only_fields = [
            'id', 'current_requests', 'current_tokens', 'current_cost_usd',
            'requests_percentage', 'tokens_percentage', 'cost_percentage',
            'is_exceeded'
        ]

class EmailToTaskSerializer(serializers.Serializer):
    """Serializer for email-to-task conversion requests"""
    email_content = serializers.CharField()
    sender_email = serializers.EmailField(required=False)
    sender_name = serializers.CharField(max_length=255, required=False)
    subject = serializers.CharField(max_length=500, required=False)
    additional_context = serializers.JSONField(default=dict, required=False)
    
    def validate_email_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Email content is too short")
        return value

class SocialContentGenerationSerializer(serializers.Serializer):
    """Serializer for social media content generation"""
    business_update = serializers.CharField()
    platform = serializers.ChoiceField(
        choices=[
            ('facebook', 'Facebook'),
            ('instagram', 'Instagram'),
            ('tiktok', 'TikTok'),
            ('linkedin', 'LinkedIn'),
            ('twitter', 'Twitter')
        ],
        default='facebook'
    )
    tone = serializers.ChoiceField(
        choices=[
            ('professional', 'Professional'),
            ('casual', 'Casual'),
            ('friendly', 'Friendly'),
            ('excited', 'Excited'),
            ('informative', 'Informative')
        ],
        default='friendly'
    )
    include_hashtags = serializers.BooleanField(default=True)
    include_call_to_action = serializers.BooleanField(default=True)
    target_audience = serializers.CharField(max_length=255, required=False)
    
    def validate_business_update(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Business update is too short")
        return value

class CustomAIRequestSerializer(serializers.Serializer):
    """Serializer for custom AI requests using templates"""
    template_id = serializers.IntegerField()
    input_variables = serializers.JSONField()
    custom_instructions = serializers.CharField(required=False, allow_blank=True)
    
    def validate_template_id(self, value):
        try:
            template = AITemplate.objects.get(id=value, is_active=True)
            user = self.context['request'].user
            
            # Check if user can access premium templates
            if template.is_premium and user.subscription_tier == 'starter':
                raise serializers.ValidationError(
                    "Premium templates require Business or Pro subscription"
                )
            return value
        except AITemplate.DoesNotExist:
            raise serializers.ValidationError("Template not found or inactive")

class TextAnalysisSerializer(serializers.Serializer):
    """Serializer for text analysis requests"""
    text = serializers.CharField()
    analysis_type = serializers.ChoiceField(
        choices=[
            ('sentiment', 'Sentiment Analysis'),
            ('summary', 'Text Summarization'),
            ('keywords', 'Keyword Extraction'),
            ('translation', 'Translation'),
            ('categorization', 'Text Categorization')
        ]
    )
    target_language = serializers.ChoiceField(
        choices=[('en', 'English'), ('tl', 'Tagalog'), ('auto', 'Auto-detect')],
        default='auto',
        required=False
    )
    
    def validate_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Text is too short for analysis")
        if len(value) > 10000:
            raise serializers.ValidationError("Text is too long (max 10,000 characters)")
        return value

class AIUsageStatsSerializer(serializers.Serializer):
    """Serializer for AI usage statistics"""
    total_requests = serializers.IntegerField()
    successful_requests = serializers.IntegerField()
    failed_requests = serializers.IntegerField()
    total_tokens = serializers.IntegerField()
    total_cost_php = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_month_requests = serializers.IntegerField()
    current_month_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    quota_usage_percentage = serializers.FloatField()
    most_used_request_type = serializers.CharField()
    average_response_time = serializers.FloatField()
    
class AIHealthCheckSerializer(serializers.Serializer):
    """Serializer for AI service health check"""
    service_status = serializers.CharField()
    available_models = serializers.ListField()
    response_time_ms = serializers.IntegerField()
    last_check = serializers.DateTimeField()
    error_message = serializers.CharField(required=False)