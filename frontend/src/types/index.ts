// Auth Types
export interface User {
  id: number;
  email: string;
  username: string;
  company_name: string;
  subscription_tier: 'starter' | 'business' | 'pro';
  monthly_ai_calls: number;
  business_type: string;
  preferred_language: 'en' | 'tl';
  created_at: string;
}

export interface BusinessProfile {
  id: number;
  industry: string;
  employee_count: string;
  city: string;
  region: string;
  business_description: string;
  automation_goals: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

// AI Types
export interface AIModel {
  id: number;
  name: string;
  model_id: string;
  model_type: string;
  capability_level: string;
  provider_name: string;
  supports_tagalog: boolean;
  supports_filipino_context: boolean;
  min_subscription_tier: string;
  cost_estimate: number;
}

export interface AIRequest {
  id: string;
  model_name: string;
  request_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  cost_php: number;
  response_time_ms: number;
  created_at: string;
  completed_at?: string;
}

export interface AIUsageStats {
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  total_tokens: number;
  total_cost_php: number;
  current_month_requests: number;
  current_month_cost: number;
  quota_usage_percentage: number;
  most_used_request_type?: string;
  average_response_time: number;
}

// Automation Types
export interface AutomationWorkflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'disabled';
  trigger_type: string;
  total_executions: number;
  success_rate: number;
  last_executed?: string;
  actions_count: number;
  created_at: string;
}

export interface AutomationAction {
  id: number;
  name: string;
  action_type: string;
  action_config: Record<string, any>;
  order: number;
  ai_enhanced: boolean;
  is_conditional: boolean;
}

export interface WorkflowExecution {
  id: string;
  workflow_name: string;
  status: string;
  started_at: string;
  completed_at?: string;
  duration_seconds?: number;
  ai_calls_made: number;
  success_percentage: number;
}

// Integration Types
export interface Integration {
  id: string;
  name: string;
  integration_type: string;
  service_name: string;
  is_active: boolean;
  health_status: 'healthy' | 'warning' | 'error' | 'disconnected';
  success_rate: number;
  last_used?: string;
  created_at: string;
}

// UI Types
export interface DashboardStats {
  workflows: {
    total: number;
    active: number;
    paused: number;
  };
  executions: {
    total: number;
    successful: number;
    success_rate: number;
  };
  ai_usage: {
    monthly_calls: number;
    limit: number;
    percentage_used: number;
  };
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Form Types
export interface LoginForm {
  email: string;
  password: string;
}

export interface RegisterForm {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  company_name: string;
  business_type: string;
}

export interface EmailToTaskForm {
  email_content: string;
  sender_email?: string;
  sender_name?: string;
  subject?: string;
}

export interface SocialContentForm {
  business_update: string;
  platform: 'facebook' | 'instagram' | 'tiktok' | 'linkedin';
  tone: 'professional' | 'casual' | 'friendly' | 'excited';
  include_hashtags: boolean;
  include_call_to_action: boolean;
}