'use client'

import { useEffect, useState } from 'react'
import { 
  BoltIcon, 
  ChartBarIcon, 
  SparklesIcon, 
  CurrencyDollarIcon,
  ClockIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline'
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/Card'
import { StatsCard } from '@/components/dashboard/StatsCard'
import { AIUsageChart } from '@/components/dashboard/AIUsageChart'
import { Button } from '@/components/ui/Button'
import { useAuthStore } from '@/store/auth'
import { formatCurrency, formatRelativeTime, getBusinessTypeIcon } from '@/lib/utils'
import { AutomationWorkflow, WorkflowExecution, AIUsageStats } from '@/types'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<any>(null)
  const [aiStats, setAiStats] = useState<AIUsageStats | null>(null)
  const [recentExecutions, setRecentExecutions] = useState<WorkflowExecution[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // TODO: Replace with actual API calls
    const mockStats = {
      workflows: { total: 5, active: 3, paused: 2 },
      executions: { total: 47, successful: 42, success_rate: 89.4 },
      ai_usage: { monthly_calls: 156, limit: 1000, percentage_used: 15.6 },
    }
    
    const mockAiStats: AIUsageStats = {
      total_requests: 156,
      successful_requests: 148,
      failed_requests: 8,
      total_tokens: 45680,
      total_cost_php: 89.50,
      current_month_requests: 156,
      current_month_cost: 89.50,
      quota_usage_percentage: 15.6,
      most_used_request_type: 'email_to_task',
      average_response_time: 1250
    }

    const mockExecutions: WorkflowExecution[] = [
      {
        id: '1',
        workflow_name: 'Email to Task - Client Inquiries',
        status: 'completed',
        started_at: new Date(Date.now() - 3600000).toISOString(),
        ai_calls_made: 1,
        success_percentage: 100
      },
      {
        id: '2', 
        workflow_name: 'Social Media Scheduler',
        status: 'completed',
        started_at: new Date(Date.now() - 7200000).toISOString(),
        ai_calls_made: 2,
        success_percentage: 100
      }
    ]

    setStats(mockStats)
    setAiStats(mockAiStats)
    setRecentExecutions(mockExecutions)
    setIsLoading(false)
  }, [])

  // Calculate usage percentage for progress bar
  const getUsagePercentage = () => {
    if (!user?.monthly_ai_calls) return 0
    const limit = user.subscription_tier === 'starter' ? 1000 : 
                  user.subscription_tier === 'business' ? 5000 : Infinity
    return Math.min((user.monthly_ai_calls / limit) * 100, 100)
  }

  const getSubscriptionLimit = () => {
    return user?.subscription_tier === 'starter' ? '1000' : 
           user?.subscription_tier === 'business' ? '5000' : '∞'
  }

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    )
  }

  const chartData = [
    { date: 'Mon', requests: 23, cost: 18.50 },
    { date: 'Tue', requests: 31, cost: 24.80 },
    { date: 'Wed', requests: 18, cost: 14.40 },
    { date: 'Thu', requests: 28, cost: 22.40 },
    { date: 'Fri', requests: 35, cost: 28.00 },
    { date: 'Sat', requests: 12, cost: 9.60 },
    { date: 'Sun', requests: 9, cost: 7.20 },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Welcome back, {user?.company_name}! {getBusinessTypeIcon(user?.business_type || 'general')}
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <Button variant="outline" size="sm">
            View Analytics
          </Button>
          <Button size="sm">
            Create Automation
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Active Workflows"
          value={stats?.workflows.active || 0}
          icon={<BoltIcon className="w-6 h-6" />}
          color="blue"
        />
        <StatsCard
          title="AI Requests"
          value={aiStats?.current_month_requests || 0}
          change={12}
          icon={<SparklesIcon className="w-6 h-6" />}
          color="purple"
        />
        <StatsCard
          title="Success Rate"
          value={`${stats?.executions.success_rate || 0}%`}
          change={5.2}
          icon={<CheckCircleIcon className="w-6 h-6" />}
          color="green"
        />
        <StatsCard
          title="Monthly Cost"
          value={formatCurrency(aiStats?.current_month_cost || 0)}
          icon={<CurrencyDollarIcon className="w-6 h-6" />}
          color="yellow"
        />
      </div>

      {/* Charts and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AIUsageChart data={chartData} />
        
        {/* Recent Workflow Executions */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Executions</CardTitle>
            <CardDescription>Latest workflow runs</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentExecutions.map((execution) => (
                <div key={execution.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{execution.workflow_name}</p>
                    <p className="text-sm text-gray-500">
                      {formatRelativeTime(execution.started_at)} • {execution.ai_calls_made} AI calls
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      execution.status === 'completed' 
                        ? 'text-green-700 bg-green-100' 
                        : 'text-yellow-700 bg-yellow-100'
                    }`}>
                      {execution.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Usage Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>AI Usage Summary</CardTitle>
            <CardDescription>Your AI automation usage this month</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Monthly AI Calls</span>
                <span className="font-medium">
                  {user?.monthly_ai_calls} / {getSubscriptionLimit()}
                </span>
              </div>
              
              {/* Progress bar using CSS custom property */}
              <div 
                className="w-full bg-gray-200 rounded-full h-2"
                style={{ '--usage-width': `${getUsagePercentage()}%` } as React.CSSProperties}
              >
                <div className="h-2 bg-primary-600 rounded-full transition-all duration-300 usage-progress" />
              </div>
              
              <div className="grid grid-cols-2 gap-4 pt-4">
                <div>
                  <p className="text-sm text-gray-600">Average Response Time</p>
                  <p className="text-lg font-semibold">{aiStats?.average_response_time}ms</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Success Rate</p>
                  <p className="text-lg font-semibold">
                    {aiStats ? Math.round((aiStats.successful_requests / aiStats.total_requests) * 100) : 0}%
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button variant="outline" className="w-full justify-start">
              <SparklesIcon className="w-4 h-4 mr-2" />
              Process Email
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <BoltIcon className="w-4 h-4 mr-2" />
              Create Workflow
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <ChartBarIcon className="w-4 h-4 mr-2" />
              View Analytics
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}