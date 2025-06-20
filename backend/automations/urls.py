from django.urls import path
from . import views

urlpatterns = [
    # Workflows
    path('workflows/', views.AutomationWorkflowListView.as_view(), name='workflow-list'),
    path('workflows/<uuid:pk>/', views.AutomationWorkflowDetailView.as_view(), name='workflow-detail'),
    path('workflows/<uuid:workflow_id>/toggle/', views.toggle_workflow_status, name='workflow-toggle'),
    path('workflows/<uuid:workflow_id>/execute/', views.execute_workflow_manually, name='workflow-execute'),
    
    # Actions
    path('workflows/<uuid:workflow_id>/actions/', views.AutomationActionListView.as_view(), name='action-list'),
    path('workflows/<uuid:workflow_id>/actions/<int:pk>/', views.AutomationActionDetailView.as_view(), name='action-detail'),
    
    # Executions
    path('executions/', views.WorkflowExecutionListView.as_view(), name='execution-list'),
    path('executions/<uuid:pk>/', views.WorkflowExecutionDetailView.as_view(), name='execution-detail'),
    
    # Templates
    path('templates/', views.AutomationTemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', views.AutomationTemplateDetailView.as_view(), name='template-detail'),
    path('templates/create-workflow/', views.create_workflow_from_template, name='create-from-template'),
    
    # Dashboard
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
]