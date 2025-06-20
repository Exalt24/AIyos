'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'react-hot-toast'
import { 
  EnvelopeIcon, 
  ClockIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { aiService } from '@/services/ai'
import { formatCurrency } from '@/lib/utils'

const emailToTaskSchema = z.object({
  email_content: z.string().min(10, 'Email content must be at least 10 characters'),
  sender_email: z.string().email().optional().or(z.literal('')),
  sender_name: z.string().optional(),
  subject: z.string().optional(),
})

type EmailToTaskForm = z.infer<typeof emailToTaskSchema>

interface TaskResult {
  title: string
  description: string
  priority: number
  due_date: string
  category: string
  estimated_duration: string
  required_actions: string[]
  filipino_context?: string
}

export default function EmailToTaskPage() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [result, setResult] = useState<TaskResult | null>(null)
  const [processingInfo, setProcessingInfo] = useState<{
    cost_php: number
    tokens_used: number
    request_id: string
  } | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch
  } = useForm<EmailToTaskForm>({
    resolver: zodResolver(emailToTaskSchema),
  })

  const emailContent = watch('email_content', '')

  const onSubmit = async (data: EmailToTaskForm) => {
    setIsProcessing(true)
    setResult(null)
    setProcessingInfo(null)

    try {
      const response = await aiService.emailToTask(data)
      
      if (response.success) {
        setResult(response.task)
        setProcessingInfo({
          cost_php: response.cost_php,
          tokens_used: response.tokens_used,
          request_id: response.request_id
        })
        toast.success('Email successfully converted to task! 🎉')
      } else {
        toast.error(response.error || 'Failed to process email')
      }
    } catch (error: any) {
      console.error('Email processing error:', error)
      toast.error(error.response?.data?.error || 'Failed to process email')
    } finally {
      setIsProcessing(false)
    }
  }

  const getPriorityColor = (priority: number) => {
    if (priority <= 2) return 'text-red-600 bg-red-50'
    if (priority <= 3) return 'text-yellow-600 bg-yellow-50'
    return 'text-blue-600 bg-blue-50'
  }

  const getPriorityLabel = (priority: number) => {
    if (priority === 1) return 'Urgent'
    if (priority === 2) return 'High'
    if (priority === 3) return 'Medium'
    return 'Low'
  }

  return (
    <div className="space-y-6">
      {/* Feature Description */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <EnvelopeIcon className="w-6 h-6 text-primary-600 mr-2" />
            Email to Task Converter
          </CardTitle>
          <CardDescription>
            Convert client emails into clear, actionable tasks with Filipino business context. 
            Perfect for BPO companies, consultants, and service businesses.
          </CardDescription>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Email Content</CardTitle>
            <CardDescription>
              Paste your email content below and we'll convert it to a structured task
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Content *
                </label>
                <textarea
                  {...register('email_content')}
                  rows={8}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  placeholder="Paste your email content here...

Example:
Hi John,

I hope this email finds you well. We need to schedule a meeting with our Manila team to discuss the Q1 budget approval. Can you please coordinate with the finance department and book the conference room for next Tuesday at 2 PM? We'll also need the projector and catering for 8 people.

Thanks!
Maria"
                />
                {errors.email_content && (
                  <p className="mt-1 text-sm text-red-600">{errors.email_content.message}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  {emailContent.length} characters
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Sender Email (Optional)
                  </label>
                  <input
                    {...register('sender_email')}
                    type="email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="sender@example.com"
                  />
                  {errors.sender_email && (
                    <p className="mt-1 text-sm text-red-600">{errors.sender_email.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Sender Name (Optional)
                  </label>
                  <input
                    {...register('sender_name')}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subject (Optional)
                </label>
                <input
                  {...register('subject')}
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Email subject line"
                />
              </div>

              <Button
                type="submit"
                className="w-full"
                isLoading={isProcessing}
                disabled={isProcessing || !emailContent.trim()}
              >
                {isProcessing ? 'Processing Email...' : 'Convert to Task'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Result Display */}
        <Card>
          <CardHeader>
            <CardTitle>Generated Task</CardTitle>
            <CardDescription>
              {result ? 'Your email has been converted to a structured task' : 'Task details will appear here after processing'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isProcessing && (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
                  <p className="text-gray-600">Processing email with AI...</p>
                  <p className="text-sm text-gray-500 mt-1">This usually takes 2-3 seconds</p>
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                {/* Task Header */}
                <div className="border-b border-gray-200 pb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{result.title}</h3>
                  <div className="flex items-center space-x-4 mt-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(result.priority)}`}>
                      Priority: {getPriorityLabel(result.priority)}
                    </span>
                    <div className="flex items-center text-sm text-gray-600">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {result.estimated_duration}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <CheckCircleIcon className="w-4 h-4 mr-1" />
                      {result.category}
                    </div>
                  </div>
                </div>

                {/* Task Details */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                  <p className="text-gray-700 text-sm leading-relaxed">{result.description}</p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Due Date</h4>
                  <p className="text-gray-700 text-sm">{result.due_date}</p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Required Actions</h4>
                  <ul className="space-y-1">
                    {result.required_actions.map((action, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-700">
                        <span className="text-primary-600 mr-2">•</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>

                {result.filipino_context && (
                  <div className="bg-filipino-yellow/10 border border-filipino-yellow/20 rounded-lg p-3">
                    <h4 className="font-medium text-gray-900 mb-1 flex items-center">
                      <ExclamationTriangleIcon className="w-4 h-4 text-filipino-yellow mr-1" />
                      Filipino Business Context
                    </h4>
                    <p className="text-sm text-gray-700">{result.filipino_context}</p>
                  </div>
                )}

                {/* Processing Info */}
                {processingInfo && (
                  <div className="border-t border-gray-200 pt-4">
                    <div className="flex justify-between items-center text-sm text-gray-600">
                      <span>Processing Cost:</span>
                      <span className="font-medium">{formatCurrency(processingInfo.cost_php)}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm text-gray-600">
                      <span>Tokens Used:</span>
                      <span className="font-medium">{processingInfo.tokens_used.toLocaleString()}</span>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-3 pt-4">
                  <Button size="sm" className="flex-1">
                    Create Workflow
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    Save as Template
                  </Button>
                </div>
              </div>
            )}

            {!result && !isProcessing && (
              <div className="text-center py-12 text-gray-500">
                <EnvelopeIcon className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>Enter email content and click "Convert to Task" to see results</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Tips & Examples */}
      <Card>
        <CardHeader>
          <CardTitle>Tips for Better Results</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">📧 Email Types</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Client inquiries</li>
                <li>• Meeting requests</li>
                <li>• Project updates</li>
                <li>• Support tickets</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">🇵🇭 Filipino Context</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Considers PH business hours</li>
                <li>• Understands Tagalog terms</li>
                <li>• Local compliance aware</li>
                <li>• Cultural context sensitive</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">⚡ Best Practices</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Include full email content</li>
                <li>• Add sender information</li>
                <li>• Provide context when needed</li>
                <li>• Review generated tasks</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}