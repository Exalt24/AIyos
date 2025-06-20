from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()

class AIProvider(models.Model):
    """AI service providers and model configurations"""
    
    PROVIDER_TYPES = [
        ('openrouter', 'OpenRouter'),
        ('openai', 'OpenAI Direct'),
        ('anthropic', 'Anthropic Direct'),
        ('google', 'Google AI'),
    ]
    
    name = models.CharField(max_length=100)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)
    api_endpoint = models.URLField()
    is_active = models.BooleanField(default=True)
    
    # Cost configuration
    cost_per_input_token = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    cost_per_output_token = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    
    # Rate limits
    requests_per_minute = models.IntegerField(default=60)
    tokens_per_minute = models.IntegerField(default=50000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_providers'
        verbose_name = 'AI Provider'
        verbose_name_plural = 'AI Providers'
    
    def __str__(self):
        return f"{self.name} ({self.provider_type})"

class AIModel(models.Model):
    """Available AI models for different tasks"""
    
    MODEL_TYPES = [
        ('chat', 'Chat Completion'),
        ('embedding', 'Text Embedding'),
        ('image', 'Image Generation'),
        ('audio', 'Audio Processing'),
    ]
    
    CAPABILITY_LEVELS = [
        ('basic', 'Basic'),
        ('advanced', 'Advanced'),
        ('premium', 'Premium'),
    ]
    
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE, related_name='models')
    
    # Model details
    name = models.CharField(max_length=100)
    model_id = models.CharField(max_length=200, help_text="API model identifier")
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    capability_level = models.CharField(max_length=20, choices=CAPABILITY_LEVELS)
    
    # Context and capabilities
    max_context_tokens = models.IntegerField(default=4000)
    max_output_tokens = models.IntegerField(default=1000)
    supports_functions = models.BooleanField(default=False)
    supports_streaming = models.BooleanField(default=False)
    
    # Filipino context capabilities
    supports_tagalog = models.BooleanField(default=False)
    supports_filipino_context = models.BooleanField(default=False)
    
    # Subscription requirements
    min_subscription_tier = models.CharField(
        max_length=20,
        choices=[('starter', 'Starter'), ('business', 'Business'), ('pro', 'Pro')],
        default='starter'
    )
    
    # Performance metrics
    average_response_time_ms = models.IntegerField(default=1000)
    reliability_score = models.FloatField(default=0.95)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_models'
        unique_together = ['provider', 'model_id']
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
    
    def __str__(self):
        return f"{self.name} ({self.provider.name})"
    
    @property
    def cost_per_request_estimate(self):
        """Rough cost estimate for average request"""
        avg_input_tokens = 500
        avg_output_tokens = 200
        input_cost = float(self.provider.cost_per_input_token) * avg_input_tokens
        output_cost = float(self.provider.cost_per_output_token) * avg_output_tokens
        return input_cost + output_cost

class AIRequest(models.Model):
    """Track all AI requests for monitoring and billing"""
    
    REQUEST_TYPES = [
        ('email_to_task', 'Email to Task Conversion'),
        ('content_generation', 'Content Generation'),
        ('text_analysis', 'Text Analysis'),
        ('translation', 'Translation'),
        ('summarization', 'Summarization'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('data_extraction', 'Data Extraction'),
        ('workflow_optimization', 'Workflow Optimization'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_requests')
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='requests')
    
    # Request details
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Input/Output
    input_data = models.JSONField(help_text="Original input data")
    processed_input = models.TextField(help_text="Processed prompt sent to AI")
    output_data = models.JSONField(default=dict, help_text="AI response data")
    
    # Token usage
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    
    # Cost tracking
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    cost_php = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    
    # Performance
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    error_code = models.CharField(max_length=100, blank=True)
    retry_count = models.IntegerField(default=0)
    
    # Context
    workflow_execution = models.UUIDField(null=True, blank=True, help_text="Related workflow execution")
    user_context = models.JSONField(default=dict, help_text="User business context")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'ai_requests'
        ordering = ['-created_at']
        verbose_name = 'AI Request'
        verbose_name_plural = 'AI Requests'
    
    def __str__(self):
        return f"{self.user.company_name} - {self.get_request_type_display()} ({self.status})"
    
    @property
    def duration_seconds(self):
        if self.completed_at and self.created_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None

class AITemplate(models.Model):
    """Pre-built AI prompts for Filipino business scenarios"""
    
    TEMPLATE_CATEGORIES = [
        ('email_processing', 'Email Processing'),
        ('customer_service', 'Customer Service'),
        ('content_creation', 'Content Creation'),
        ('data_analysis', 'Data Analysis'),
        ('translation', 'Translation'),
        ('compliance', 'Government Compliance'),
        ('sales_marketing', 'Sales & Marketing'),
    ]
    
    BUSINESS_CONTEXTS = [
        ('bpo', 'BPO Company'),
        ('real_estate', 'Real Estate'),
        ('ecommerce', 'E-commerce'),
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail'),
        ('agency', 'Agency'),
        ('ofw_family', 'OFW Family'),
        ('general', 'General Business'),
    ]
    
    # Template info
    name = models.CharField(max_length=255)
    tagalog_name = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=TEMPLATE_CATEGORIES)
    business_context = models.CharField(max_length=50, choices=BUSINESS_CONTEXTS)
    
    # Template content
    system_prompt = models.TextField(help_text="System prompt for AI model")
    user_prompt_template = models.TextField(help_text="Template with variables like {email_content}")
    example_input = models.JSONField(default=dict, help_text="Example input data")
    example_output = models.JSONField(default=dict, help_text="Expected output format")
    
    # Configuration
    recommended_model_type = models.CharField(max_length=20, default='chat')
    max_tokens = models.IntegerField(default=500)
    temperature = models.FloatField(default=0.7)
    
    # Filipino context
    supports_tagalog = models.BooleanField(default=True)
    supports_mixed_language = models.BooleanField(default=True)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_templates'
        ordering = ['-usage_count']
        verbose_name = 'AI Template'
        verbose_name_plural = 'AI Templates'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def increment_usage(self, success=True):
        self.usage_count += 1
        if success and self.usage_count > 0:
            # Recalculate success rate (simplified)
            current_successes = self.success_rate * (self.usage_count - 1) / 100
            new_successes = current_successes + 1
            self.success_rate = (new_successes / self.usage_count) * 100
        self.save(update_fields=['usage_count', 'success_rate'])

class AIUsageQuota(models.Model):
    """Track AI usage quotas by user and time period"""
    
    PERIOD_TYPES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_quotas')
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPES)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Usage limits
    max_requests = models.IntegerField()
    max_tokens = models.IntegerField()
    max_cost_usd = models.DecimalField(max_digits=10, decimal_places=4)
    
    # Current usage
    current_requests = models.IntegerField(default=0)
    current_tokens = models.IntegerField(default=0)
    current_cost_usd = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    
    # Status
    is_exceeded = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_usage_quotas'
        unique_together = ['user', 'period_type', 'period_start']
        verbose_name = 'AI Usage Quota'
        verbose_name_plural = 'AI Usage Quotas'
    
    def __str__(self):
        return f"{self.user.company_name} - {self.period_type} ({self.period_start.strftime('%Y-%m-%d')})"
    
    @property
    def requests_percentage(self):
        if self.max_requests == 0:
            return 0
        return min(100, (self.current_requests / self.max_requests) * 100)
    
    @property
    def tokens_percentage(self):
        if self.max_tokens == 0:
            return 0
        return min(100, (self.current_tokens / self.max_tokens) * 100)
    
    @property
    def cost_percentage(self):
        if self.max_cost_usd == 0:
            return 0
        return min(100, (float(self.current_cost_usd) / float(self.max_cost_usd)) * 100)
    
    def update_usage(self, requests=0, tokens=0, cost_usd=0):
        """Update usage counters"""
        self.current_requests += requests
        self.current_tokens += tokens
        self.current_cost_usd += cost_usd
        
        # Check if exceeded
        self.is_exceeded = (
            self.current_requests >= self.max_requests or
            self.current_tokens >= self.max_tokens or
            self.current_cost_usd >= self.max_cost_usd
        )
        
        self.save()