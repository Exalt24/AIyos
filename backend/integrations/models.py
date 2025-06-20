from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()

class Integration(models.Model):
    """Third-party service integrations for Filipino businesses"""
    
    INTEGRATION_TYPES = [
        # Communication
        ('email', 'Email (Gmail/Outlook)'),
        ('sms', 'SMS Service'),
        ('chat', 'Chat Platform'),
        
        # Philippine Payment Gateways
        ('payment', 'Payment Gateway'),
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
        ('grabpay', 'GrabPay'),
        
        # Philippine Banks
        ('bdo', 'BDO Unibank'),
        ('bpi', 'Bank of the Philippine Islands'),
        ('metrobank', 'Metrobank'),
        ('unionbank', 'UnionBank'),
        
        # CRM & Business Tools
        ('crm', 'CRM System'),
        ('calendar', 'Calendar'),
        ('storage', 'File Storage'),
        
        # Filipino Social Media & E-commerce
        ('social_media', 'Social Media'),
        ('facebook', 'Facebook/Meta Business'),
        ('instagram', 'Instagram Business'),
        ('tiktok', 'TikTok for Business'),
        
        # Local E-commerce Platforms
        ('ecommerce', 'E-commerce Platform'),
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
        ('zalora', 'Zalora'),
        
        # Government & Compliance
        ('government', 'Government Service'),
        ('bir', 'Bureau of Internal Revenue'),
        ('dti', 'Department of Trade and Industry'),
        ('sss', 'Social Security System'),
        ('philhealth', 'PhilHealth'),
        
        # Communication Tools
        ('communication', 'Communication Tool'),
        ('slack', 'Slack'),
        ('teams', 'Microsoft Teams'),
        ('discord', 'Discord'),
        
        # Other
        ('webhook', 'Custom Webhook'),
        ('api', 'Custom API'),
    ]
    
    HEALTH_STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('disconnected', 'Disconnected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')
    
    # Integration Details
    name = models.CharField(max_length=255, help_text="Custom name for this integration")
    integration_type = models.CharField(max_length=50, choices=INTEGRATION_TYPES)
    service_name = models.CharField(max_length=100, help_text="Official service name")
    service_url = models.URLField(blank=True, help_text="Service website or API endpoint")
    
    # Configuration
    config_data = models.JSONField(default=dict, help_text="Integration-specific configuration")
    is_active = models.BooleanField(default=True)
    
    # Authentication (encrypted in production)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    webhook_secret = models.CharField(max_length=255, blank=True)
    
    # OAuth Configuration
    oauth_provider = models.CharField(max_length=100, blank=True)
    oauth_scope = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Health & Monitoring
    last_health_check = models.DateTimeField(null=True, blank=True)
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, default='healthy')
    health_message = models.TextField(blank=True)
    
    # Usage Statistics
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Rate Limiting
    rate_limit_remaining = models.IntegerField(null=True, blank=True)
    rate_limit_reset = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integrations'
        unique_together = ['user', 'service_name', 'name']
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'
    
    def __str__(self):
        return f"{self.user.company_name} - {self.name} ({self.service_name})"
    
    @property
    def success_rate(self):
        if self.total_requests == 0:
            return 0
        return round((self.successful_requests / self.total_requests) * 100, 2)
    
    @property
    def is_connected(self):
        return self.health_status == 'healthy' and self.is_active
    
    @property
    def needs_reauthorization(self):
        from django.utils import timezone
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

class IntegrationLog(models.Model):
    """Log of integration requests and responses"""
    
    LOG_TYPES = [
        ('request', 'API Request'),
        ('response', 'API Response'),
        ('error', 'Error'),
        ('health_check', 'Health Check'),
        ('auth', 'Authentication'),
    ]
    
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='logs')
    
    # Log Details
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    method = models.CharField(max_length=10, blank=True)  # GET, POST, etc.
    endpoint = models.CharField(max_length=500, blank=True)
    
    # Request/Response Data
    request_data = models.JSONField(default=dict, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    
    # Error Information
    error_message = models.TextField(blank=True)
    error_code = models.CharField(max_length=100, blank=True)
    
    # Performance
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    # Context
    workflow_execution = models.UUIDField(null=True, blank=True, help_text="Related workflow execution ID")
    user_agent = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'integration_logs'
        ordering = ['-created_at']
        verbose_name = 'Integration Log'
        verbose_name_plural = 'Integration Logs'
    
    def __str__(self):
        return f"{self.integration.name} - {self.log_type} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class WebhookEndpoint(models.Model):
    """Webhook endpoints for receiving data from external services"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('disabled', 'Disabled'),
    ]
    
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='webhooks')
    
    # Webhook Configuration
    name = models.CharField(max_length=255)
    url_path = models.CharField(max_length=255, unique=True, help_text="Unique URL path for this webhook")
    secret_key = models.CharField(max_length=255, help_text="Secret key for webhook verification")
    
    # Security
    allowed_ips = models.JSONField(default=list, blank=True, help_text="Allowed IP addresses")
    require_signature = models.BooleanField(default=True)
    signature_header = models.CharField(max_length=100, default='X-Signature')
    
    # Processing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    auto_trigger_workflows = models.BooleanField(default=True)
    
    # Statistics
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    last_triggered = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'webhook_endpoints'
        verbose_name = 'Webhook Endpoint'
        verbose_name_plural = 'Webhook Endpoints'
    
    def __str__(self):
        return f"{self.integration.name} - {self.name}"
    
    @property
    def full_url(self):
        from django.conf import settings
        base_url = getattr(settings, 'WEBHOOK_BASE_URL', 'https://api.aiyos.ph')
        return f"{base_url}/webhooks/{self.url_path}/"
    
    @property
    def success_rate(self):
        if self.total_requests == 0:
            return 0
        return round((self.successful_requests / self.total_requests) * 100, 2)