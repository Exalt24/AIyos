from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import AIProvider, AIModel, AIRequest, AITemplate, AIUsageQuota
from .serializers import (
    AIModelSerializer, AIRequestSerializer, AITemplateSerializer,
    AIUsageQuotaSerializer, EmailToTaskSerializer, SocialContentGenerationSerializer,
    CustomAIRequestSerializer, TextAnalysisSerializer, AIUsageStatsSerializer,
    AIHealthCheckSerializer
)
from .services import get_ai_service

class AIModelListView(generics.ListAPIView):
    """List available AI models for user's subscription tier"""
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['model_type', 'capability_level', 'supports_tagalog']
    ordering_fields = ['name', 'average_response_time_ms']
    ordering = ['capability_level', 'name']
    
    def get_queryset(self):
        user = self.request.user
        # Filter models based on subscription tier
        queryset = AIModel.objects.filter(is_active=True)
        
        if user.subscription_tier == 'starter':
            queryset = queryset.filter(min_subscription_tier='starter')
        elif user.subscription_tier == 'business':
            queryset = queryset.filter(min_subscription_tier__in=['starter', 'business'])
        # Pro users can access all models
        
        return queryset

class AIRequestListView(generics.ListAPIView):
    """List user's AI requests"""
    serializer_class = AIRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['request_type', 'status', 'model']
    ordering_fields = ['created_at', 'response_time_ms', 'total_tokens']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user).select_related('model')

class AIRequestDetailView(generics.RetrieveAPIView):
    """Get detailed AI request information"""
    serializer_class = AIRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user).select_related('model')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def email_to_task(request):
    """Convert email to actionable task using AI"""
    serializer = EmailToTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    ai_service = get_ai_service(user=request.user)
    
    # Check if user can use AI
    if not request.user.can_use_ai():
        return Response(
            {'error': 'AI usage limit exceeded for your subscription'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    
    try:
        # Prepare user context
        user_context = {
            'sender_email': serializer.validated_data.get('sender_email'),
            'sender_name': serializer.validated_data.get('sender_name'),
            'subject': serializer.validated_data.get('subject'),
            **serializer.validated_data.get('additional_context', {})
        }
        
        # Process email
        result = ai_service.process_email_to_task(
            email_content=serializer.validated_data['email_content'],
            user_context=user_context
        )
        
        return Response(result)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_social_content(request):
    """Generate social media content using AI"""
    serializer = SocialContentGenerationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    ai_service = get_ai_service(user=request.user)
    
    if not request.user.can_use_ai():
        return Response(
            {'error': 'AI usage limit exceeded for your subscription'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    
    try:
        # Prepare user context
        user_context = {
            'platform': serializer.validated_data['platform'],
            'tone': serializer.validated_data['tone'],
            'include_hashtags': serializer.validated_data['include_hashtags'],
            'include_call_to_action': serializer.validated_data['include_call_to_action'],
            'target_audience': serializer.validated_data.get('target_audience', '')
        }
        
        # Generate content
        result = ai_service.generate_filipino_social_content(
            business_update=serializer.validated_data['business_update'],
            platform=serializer.validated_data['platform'],
            user_context=user_context
        )
        
        return Response(result)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def custom_ai_request(request):
    """Make custom AI request using templates"""
    serializer = CustomAIRequestSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    if not request.user.can_use_ai():
        return Response(
            {'error': 'AI usage limit exceeded for your subscription'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    
    try:
        template = AITemplate.objects.get(id=serializer.validated_data['template_id'])
        ai_service = get_ai_service(user=request.user)
        
        # Build prompt from template
        input_variables = serializer.validated_data['input_variables']
        custom_instructions = serializer.validated_data.get('custom_instructions', '')
        
        # Format template with variables
        user_prompt = template.user_prompt_template.format(**input_variables)
        if custom_instructions:
            user_prompt += f"\n\nAdditional instructions: {custom_instructions}"
        
        # Create AI request record
        ai_request = AIRequest.objects.create(
            user=request.user,
            model=ai_service.get_available_model(request.user.subscription_tier),
            request_type='custom',
            status='processing',
            input_data={
                'template_id': template.id,
                'input_variables': input_variables,
                'custom_instructions': custom_instructions
            }
        )
        
        # TODO: Implement generic AI request processing
        # For now, return mock response
        
        result = {
            'success': True,
            'response': f"Processed using template: {template.name}",
            'request_id': ai_request.id
        }
        
        # Increment template usage
        template.increment_usage(success=True)
        
        return Response(result)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analyze_text(request):
    """Analyze text using AI"""
    serializer = TextAnalysisSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    if not request.user.can_use_ai():
        return Response(
            {'error': 'AI usage limit exceeded for your subscription'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    
    # TODO: Implement text analysis features
    # For now, return mock response
    
    analysis_type = serializer.validated_data['analysis_type']
    text = serializer.validated_data['text']
    
    result = {
        'success': True,
        'analysis_type': analysis_type,
        'result': {
            'sentiment': 'positive' if analysis_type == 'sentiment' else None,
            'summary': f"Summary of: {text[:50]}..." if analysis_type == 'summary' else None,
            'keywords': ['business', 'filipino', 'automation'] if analysis_type == 'keywords' else None
        },
        'confidence': 0.85
    }
    
    return Response(result)

class AITemplateListView(generics.ListAPIView):
    """List available AI templates"""
    serializer_class = AITemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'business_context', 'supports_tagalog', 'is_premium']
    search_fields = ['name', 'tagalog_name', 'description']
    ordering_fields = ['usage_count', 'success_rate', 'name']
    ordering = ['-usage_count']
    
    def get_queryset(self):
        user = self.request.user
        queryset = AITemplate.objects.filter(is_active=True)
        
        # Filter premium templates for starter users
        if user.subscription_tier == 'starter':
            queryset = queryset.filter(is_premium=False)
        
        return queryset

class AITemplateDetailView(generics.RetrieveAPIView):
    """Get detailed template information"""
    serializer_class = AITemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = AITemplate.objects.filter(is_active=True)
        
        if user.subscription_tier == 'starter':
            queryset = queryset.filter(is_premium=False)
        
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ai_usage_stats(request):
    """Get AI usage statistics for user"""
    user = request.user
    
    # All-time stats
    all_requests = AIRequest.objects.filter(user=user)
    total_requests = all_requests.count()
    successful_requests = all_requests.filter(status='completed').count()
    failed_requests = all_requests.filter(status='failed').count()
    
    # Aggregated stats
    usage_stats = all_requests.aggregate(
        total_tokens=Sum('total_tokens'),
        total_cost_php=Sum('cost_php'),
        avg_response_time=Avg('response_time_ms')
    )
    
    # Current month stats
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_requests = all_requests.filter(created_at__gte=current_month)
    current_month_requests = monthly_requests.count()
    monthly_cost = monthly_requests.aggregate(cost=Sum('cost_php'))['cost'] or 0
    
    # Most used request type
    most_used = all_requests.values('request_type').annotate(
        count=Count('request_type')
    ).order_by('-count').first()
    
    # Quota information
    quota_usage_percentage = (user.monthly_ai_calls / user.ai_usage_limit * 100) if user.ai_usage_limit > 0 else 0
    
    stats = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'total_tokens': usage_stats['total_tokens'] or 0,
        'total_cost_php': usage_stats['total_cost_php'] or 0,
        'current_month_requests': current_month_requests,
        'current_month_cost': monthly_cost,
        'quota_usage_percentage': quota_usage_percentage,
        'most_used_request_type': most_used['request_type'] if most_used else None,
        'average_response_time': usage_stats['avg_response_time'] or 0,
    }
    
    serializer = AIUsageStatsSerializer(stats)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ai_quota_status(request):
    """Get current AI quota status"""
    user = request.user
    
    # Get current month quota
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_end = (current_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    
    quota, created = AIUsageQuota.objects.get_or_create(
        user=user,
        period_type='monthly',
        period_start=current_month,
        defaults={
            'period_end': month_end,
            'max_requests': user.ai_usage_limit,
            'max_tokens': user.ai_usage_limit * 1000,
            'max_cost_usd': 10.00 if user.subscription_tier == 'starter' else 50.00,
        }
    )
    
    serializer = AIUsageQuotaSerializer(quota)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ai_health_check(request):
    """Check AI service health"""
    import time
    
    start_time = time.time()
    
    try:
        # Check available models
        available_models = AIModel.objects.filter(is_active=True).values_list('name', flat=True)
        
        # Mock health check - in production, you'd ping the actual AI service
        service_status = 'healthy'
        response_time_ms = int((time.time() - start_time) * 1000)
        
        health_data = {
            'service_status': service_status,
            'available_models': list(available_models),
            'response_time_ms': response_time_ms,
            'last_check': timezone.now(),
        }
        
        serializer = AIHealthCheckSerializer(health_data)
        return Response(serializer.data)
        
    except Exception as e:
        health_data = {
            'service_status': 'error',
            'available_models': [],
            'response_time_ms': int((time.time() - start_time) * 1000),
            'last_check': timezone.now(),
            'error_message': str(e)
        }
        
        serializer = AIHealthCheckSerializer(health_data)
        return Response(serializer.data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ai_request_types(request):
    """Get available AI request types"""
    request_types = [
        {
            'type': 'email_to_task',
            'name': 'Email to Task',
            'description': 'Convert emails into actionable tasks',
            'icon': 'mail',
            'popular': True,
            'filipino_optimized': True
        },
        {
            'type': 'content_generation',
            'name': 'Social Media Content',
            'description': 'Generate social media posts',
            'icon': 'megaphone',
            'popular': True,
            'filipino_optimized': True
        },
        {
            'type': 'text_analysis',
            'name': 'Text Analysis',
            'description': 'Analyze sentiment, extract keywords, summarize',
            'icon': 'analytics',
            'popular': False,
            'filipino_optimized': True
        },
        {
            'type': 'translation',
            'name': 'Translation',
            'description': 'Translate between English and Tagalog',
            'icon': 'language',
            'popular': False,
            'filipino_optimized': True
        },
        {
            'type': 'custom',
            'name': 'Custom Request',
            'description': 'Use templates for specific business needs',
            'icon': 'settings',
            'popular': False,
            'filipino_optimized': False
        }
    ]
    
    return Response(request_types)