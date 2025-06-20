from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import AutomationWorkflow, AutomationAction, WorkflowExecution, AutomationTemplate
from .serializers import (
    AutomationWorkflowListSerializer, AutomationWorkflowDetailSerializer,
    AutomationWorkflowCreateSerializer, AutomationActionSerializer,
    WorkflowExecutionSerializer, AutomationTemplateSerializer,
    CreateWorkflowFromTemplateSerializer
)
from django.db import models 

class AutomationWorkflowListView(generics.ListCreateAPIView):
    """List user's workflows or create new one"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'trigger_type', 'use_ai_processing']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'last_executed', 'total_executions']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return AutomationWorkflow.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AutomationWorkflowCreateSerializer
        return AutomationWorkflowListSerializer

class AutomationWorkflowDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete specific workflow"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AutomationWorkflowDetailSerializer
    
    def get_queryset(self):
        return AutomationWorkflow.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_workflow_status(request, workflow_id):
    """Toggle workflow between active/paused"""
    workflow = get_object_or_404(
        AutomationWorkflow, 
        id=workflow_id, 
        user=request.user
    )
    
    if workflow.status == 'active':
        workflow.status = 'paused'
        message = 'Workflow paused successfully'
    elif workflow.status == 'paused':
        workflow.status = 'active'
        message = 'Workflow activated successfully'
    else:
        return Response(
            {'error': 'Cannot toggle disabled workflow'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    workflow.save()
    
    return Response({
        'message': message,
        'status': workflow.status
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def execute_workflow_manually(request, workflow_id):
    """Manually trigger workflow execution"""
    workflow = get_object_or_404(
        AutomationWorkflow, 
        id=workflow_id, 
        user=request.user
    )
    
    if workflow.status != 'active':
        return Response(
            {'error': 'Workflow must be active to execute'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check AI usage limits
    if workflow.use_ai_processing and not request.user.can_use_ai():
        return Response(
            {'error': 'AI usage limit exceeded for your subscription'}, 
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    
    # Create execution record
    execution = WorkflowExecution.objects.create(
        workflow=workflow,
        trigger_data=request.data.get('trigger_data', {}),
        status='pending'
    )
    
    # TODO: Queue for background processing with Celery
    # execute_workflow_task.delay(execution.id)
    
    return Response({
        'message': 'Workflow execution queued',
        'execution_id': execution.id
    }, status=status.HTTP_202_ACCEPTED)

class AutomationActionListView(generics.ListCreateAPIView):
    """List and create actions for a workflow"""
    serializer_class = AutomationActionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        workflow_id = self.kwargs['workflow_id']
        workflow = get_object_or_404(
            AutomationWorkflow, 
            id=workflow_id, 
            user=self.request.user
        )
        return workflow.actions.all()
    
    def perform_create(self, serializer):
        workflow_id = self.kwargs['workflow_id']
        workflow = get_object_or_404(
            AutomationWorkflow, 
            id=workflow_id, 
            user=self.request.user
        )
        serializer.save(workflow=workflow)

class AutomationActionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete specific action"""
    serializer_class = AutomationActionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        workflow_id = self.kwargs['workflow_id']
        workflow = get_object_or_404(
            AutomationWorkflow, 
            id=workflow_id, 
            user=self.request.user
        )
        return workflow.actions.all()

class WorkflowExecutionListView(generics.ListAPIView):
    """List workflow executions"""
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'workflow']
    ordering_fields = ['started_at', 'duration_seconds']
    ordering = ['-started_at']
    
    def get_queryset(self):
        return WorkflowExecution.objects.filter(
            workflow__user=self.request.user
        ).select_related('workflow')

class WorkflowExecutionDetailView(generics.RetrieveAPIView):
    """Get detailed execution information"""
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WorkflowExecution.objects.filter(
            workflow__user=self.request.user
        ).select_related('workflow')

class AutomationTemplateListView(generics.ListAPIView):
    """List available automation templates"""
    serializer_class = AutomationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_type', 'category', 'is_featured', 'is_premium']
    search_fields = ['name', 'tagalog_name', 'description']
    ordering_fields = ['usage_count', 'rating', 'created_at']
    ordering = ['-is_featured', '-usage_count']
    
    def get_queryset(self):
        user = self.request.user
        queryset = AutomationTemplate.objects.all()
        
        # Filter premium templates based on subscription
        if user.subscription_tier == 'starter':
            queryset = queryset.filter(is_premium=False)
        
        return queryset

class AutomationTemplateDetailView(generics.RetrieveAPIView):
    """Get detailed template information"""
    serializer_class = AutomationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = AutomationTemplate.objects.all()
        
        # Filter premium templates based on subscription
        if user.subscription_tier == 'starter':
            queryset = queryset.filter(is_premium=False)
        
        return queryset

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_workflow_from_template(request):
    """Create workflow from template"""
    serializer = CreateWorkflowFromTemplateSerializer(
        data=request.data, 
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    
    template = AutomationTemplate.objects.get(id=serializer.validated_data['template_id'])
    
    # Create workflow from template
    workflow = AutomationWorkflow.objects.create(
        user=request.user,
        name=serializer.validated_data['workflow_name'],
        description=f"Created from template: {template.name}",
        trigger_type=template.workflow_config.get('trigger_type', 'manual'),
        trigger_config=template.workflow_config.get('trigger_config', {}),
        ai_instructions=template.workflow_config.get('ai_instructions', ''),
        use_ai_processing=template.workflow_config.get('use_ai_processing', True),
        language_context=template.workflow_config.get('language_context', 'mixed')
    )
    
    # Create actions from template
    for action_config in template.workflow_config.get('actions', []):
        AutomationAction.objects.create(
            workflow=workflow,
            name=action_config.get('name', ''),
            action_type=action_config.get('action_type'),
            action_config=action_config.get('action_config', {}),
            order=action_config.get('order', 0),
            ai_enhanced=action_config.get('ai_enhanced', False),
            ai_prompt_template=action_config.get('ai_prompt_template', '')
        )
    
    # Increment template usage
    template.increment_usage()
    
    return Response({
        'message': 'Workflow created successfully from template',
        'workflow_id': workflow.id,
        'workflow': AutomationWorkflowDetailSerializer(workflow).data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for user"""
    user = request.user
    
    workflows = AutomationWorkflow.objects.filter(user=user)
    executions = WorkflowExecution.objects.filter(workflow__user=user)
    
    # Calculate stats
    total_workflows = workflows.count()
    active_workflows = workflows.filter(status='active').count()
    total_executions = executions.count()
    successful_executions = executions.filter(status='completed').count()
    
    # Recent executions
    recent_executions = executions.order_by('-started_at')[:10]
    
    # AI usage this month
    from django.utils import timezone
    from datetime import datetime
    
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_ai_calls = executions.filter(
        started_at__gte=current_month
    ).aggregate(
        total_calls=models.Sum('ai_calls_made')
    )['total_calls'] or 0
    
    stats = {
        'workflows': {
            'total': total_workflows,
            'active': active_workflows,
            'paused': workflows.filter(status='paused').count(),
            'disabled': workflows.filter(status='disabled').count(),
        },
        'executions': {
            'total': total_executions,
            'successful': successful_executions,
            'failed': executions.filter(status='failed').count(),
            'success_rate': round((successful_executions / total_executions * 100), 2) if total_executions > 0 else 0,
        },
        'ai_usage': {
            'monthly_calls': monthly_ai_calls,
            'user_monthly_calls': user.monthly_ai_calls,
            'limit': user.ai_usage_limit,
            'percentage_used': round((user.monthly_ai_calls / user.ai_usage_limit * 100), 2) if user.ai_usage_limit > 0 else 0,
        },
        'recent_executions': WorkflowExecutionSerializer(recent_executions, many=True).data
    }
    
    return Response(stats)