from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()

class AutomationWorkflow(models.Model):
    """Main automation workflow model for Filipino businesses"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('disabled', 'Disabled'),
    ]
    
    TRIGGER_TYPES = [
        ('email', 'Email Received'),
        ('form_submission', 'Form Submission'),
        ('payment', 'Payment Received'),
        ('schedule', 'Scheduled Trigger'),
        ('webhook', 'Webhook'),
        ('manual', 'Manual Trigger'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflows')
    
    # Basic Info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Trigger Configuration
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    trigger_config = models.JSONField(default=dict, help_text="Trigger-specific configuration")
    
    # AI Processing
    ai_instructions = models.TextField(
        blank=True,
        help_text="Custom instructions for AI processing in English/Tagalog"
    )
    use_ai_processing = models.BooleanField(default=True)
    ai_model_preference = models.CharField(
        max_length=50,
        choices=[('auto', 'Auto (based on subscription)'), ('free', 'DeepSeek R1'), ('business', 'GPT-4o-mini'), ('premium', 'Claude 3.5')],
        default='auto'
    )
    
    # Statistics
    total_executions = models.IntegerField(default=0)
    successful_executions = models.IntegerField(default=0)
    failed_executions = models.IntegerField(default=0)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    # Business Context (Filipino-specific)
    business_hours_only = models.BooleanField(default=True, help_text="Run only during Philippine business hours")
    language_context = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('tl', 'Tagalog'), ('mixed', 'English + Tagalog')],
        default='mixed'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'automation_workflows'
        ordering = ['-created_at']
        verbose_name = 'Automation Workflow'
        verbose_name_plural = 'Automation Workflows'
    
    def __str__(self):
        return f"{self.name} ({self.user.company_name})"
    
    @property
    def success_rate(self):
        if self.total_executions == 0:
            return 0
        return round((self.successful_executions / self.total_executions) * 100, 2)
    
    @property
    def is_running(self):
        return self.status == 'active'

class AutomationAction(models.Model):
    """Individual actions within a workflow"""
    
    ACTION_TYPES = [
        # Core Actions
        ('create_task', 'Create Task'),
        ('send_email', 'Send Email'),
        ('send_sms', 'Send SMS'),
        
        # Calendar & Scheduling
        ('create_calendar_event', 'Create Calendar Event'),
        ('schedule_reminder', 'Schedule Reminder'),
        
        # CRM & Business
        ('update_crm', 'Update CRM'),
        ('create_lead', 'Create Lead'),
        ('update_contact', 'Update Contact'),
        
        # Filipino Business Specific
        ('gcash_payment_reminder', 'GCash Payment Reminder'),
        ('generate_bir_reminder', 'Generate BIR Tax Reminder'),
        ('dti_compliance_check', 'DTI Compliance Check'),
        
        # Social Media (Filipino platforms)
        ('post_facebook', 'Post to Facebook'),
        ('post_instagram', 'Post to Instagram'),
        ('post_tiktok', 'Post to TikTok'),
        
        # E-commerce (Local platforms)
        ('update_shopee_inventory', 'Update Shopee Inventory'),
        ('update_lazada_inventory', 'Update Lazada Inventory'),
        ('process_shopee_order', 'Process Shopee Order'),
        
        # AI & Content
        ('generate_content', 'Generate AI Content'),
        ('translate_content', 'Translate Content'),
        ('analyze_sentiment', 'Analyze Sentiment'),
        
        # Integration & Webhook
        ('webhook', 'Send Webhook'),
        ('api_call', 'Make API Call'),
        ('file_upload', 'Upload File'),
        
        # Notifications
        ('send_notification', 'Send In-App Notification'),
        ('send_slack_message', 'Send Slack Message'),
        ('send_teams_message', 'Send Teams Message'),
    ]
    
    workflow = models.ForeignKey(
        AutomationWorkflow, 
        on_delete=models.CASCADE, 
        related_name='actions'
    )
    
    # Action Configuration
    name = models.CharField(max_length=255, help_text="Descriptive name for this action")
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    action_config = models.JSONField(default=dict, help_text="Action-specific configuration")
    order = models.IntegerField(default=0, help_text="Order of execution")
    
    # Conditional Logic
    conditions = models.JSONField(default=dict, blank=True, help_text="Conditions for execution")
    is_conditional = models.BooleanField(default=False)
    
    # AI Enhancement
    ai_enhanced = models.BooleanField(default=False)
    ai_prompt_template = models.TextField(blank=True, help_text="AI prompt template for this action")
    
    # Error Handling
    retry_on_failure = models.BooleanField(default=True)
    max_retries = models.IntegerField(default=3)
    
    # Timing
    delay_seconds = models.IntegerField(default=0, help_text="Delay before executing this action")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'automation_actions'
        ordering = ['order']
        verbose_name = 'Automation Action'
        verbose_name_plural = 'Automation Actions'
    
    def __str__(self):
        return f"{self.workflow.name} - {self.name}"

class WorkflowExecution(models.Model):
    """Track individual workflow executions"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('timeout', 'Timeout'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(
        AutomationWorkflow, 
        on_delete=models.CASCADE, 
        related_name='executions'
    )
    
    # Execution Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    trigger_data = models.JSONField(default=dict, help_text="Data that triggered the workflow")
    execution_log = models.JSONField(default=list, help_text="Step-by-step execution log")
    
    # Results
    output_data = models.JSONField(default=dict, help_text="Final output data")
    error_message = models.TextField(blank=True)
    error_details = models.JSONField(default=dict, blank=True)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)
    
    # AI Usage Tracking
    ai_calls_made = models.IntegerField(default=0)
    ai_tokens_used = models.IntegerField(default=0)
    ai_cost_estimate = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    
    # Performance Metrics
    actions_completed = models.IntegerField(default=0)
    actions_failed = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'workflow_executions'
        ordering = ['-started_at']
        verbose_name = 'Workflow Execution'
        verbose_name_plural = 'Workflow Executions'
    
    def __str__(self):
        return f"{self.workflow.name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_completed(self):
        return self.status in ['completed', 'failed', 'cancelled', 'timeout']
    
    @property
    def success_percentage(self):
        total = self.actions_completed + self.actions_failed
        if total == 0:
            return 0
        return round((self.actions_completed / total) * 100, 2)

class AutomationTemplate(models.Model):
    """Pre-built automation templates for Filipino businesses"""
    
    BUSINESS_TYPES = [
        ('bpo', 'BPO Company'),
        ('real_estate', 'Real Estate'),
        ('consulting', 'Consulting'),
        ('ecommerce', 'E-commerce'),
        ('agency', 'Marketing Agency'),
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail Store'),
        ('freelancer', 'Freelancer'),
        ('ofw_family', 'OFW Family'),
        ('general', 'General Business'),
    ]
    
    TEMPLATE_CATEGORIES = [
        ('customer_service', 'Customer Service'),
        ('sales_marketing', 'Sales & Marketing'),
        ('hr_payroll', 'HR & Payroll'),
        ('finance_accounting', 'Finance & Accounting'),
        ('inventory_orders', 'Inventory & Orders'),
        ('social_media', 'Social Media'),
        ('compliance', 'Government Compliance'),
        ('communication', 'Communication'),
    ]
    
    # Template Info
    name = models.CharField(max_length=255)
    description = models.TextField()
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    category = models.CharField(max_length=50, choices=TEMPLATE_CATEGORIES)
    
    # Template Configuration
    workflow_config = models.JSONField(help_text="Complete workflow structure")
    required_integrations = models.JSONField(default=list, help_text="Required third-party integrations")
    estimated_setup_time = models.IntegerField(help_text="Minutes to setup")
    
    # Content
    setup_instructions = models.TextField(help_text="Step-by-step setup instructions")
    preview_image = models.URLField(blank=True)
    demo_video_url = models.URLField(blank=True)
    
    # Popularity & Usage
    usage_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    
    # Filipino Context
    tagalog_name = models.CharField(max_length=255, blank=True)
    tagalog_description = models.TextField(blank=True)
    
    # Meta
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False, help_text="Requires Business/Pro subscription")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'automation_templates'
        ordering = ['-is_featured', '-usage_count']
        verbose_name = 'Automation Template'
        verbose_name_plural = 'Automation Templates'
    
    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()})"
    
    def increment_usage(self):
        self.usage_count += 1
        self.save(update_fields=['usage_count'])