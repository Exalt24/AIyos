'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  EnvelopeIcon, 
  MegaphoneIcon, 
  DocumentTextIcon,
  ChartBarIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { cn } from '@/lib/utils'

const aiFeatures = [
  {
    name: 'Email to Task',
    href: '/ai/email-to-task',
    icon: EnvelopeIcon,
    description: 'Convert emails to actionable tasks',
    popular: true
  },
  {
    name: 'Social Content',
    href: '/ai/social-content',
    icon: MegaphoneIcon,
    description: 'Generate Filipino social media posts',
    popular: true
  },
  {
    name: 'Text Analysis',
    href: '/ai/text-analysis',
    icon: DocumentTextIcon,
    description: 'Analyze sentiment & extract insights',
    popular: false
  },
  {
    name: 'Usage Stats',
    href: '/ai/usage',
    icon: ChartBarIcon,
    description: 'Monitor your AI usage',
    popular: false
  }
]

export default function AILayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <SparklesIcon className="w-8 h-8 text-primary-600 mr-3" />
            AI Features
          </h1>
          <p className="text-gray-600 mt-1">
            Automate your business with AI na may Filipino context
          </p>
        </div>
      </div>

      {/* Feature Navigation */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {aiFeatures.map((feature) => {
          const isActive = pathname === feature.href
          
          return (
            <Link
              key={feature.name}
              href={feature.href}
              className={cn(
                'p-4 rounded-lg border-2 transition-all hover:shadow-md',
                isActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              )}
            >
              <div className="flex items-center space-x-3">
                <div className={cn(
                  'p-2 rounded-lg',
                  isActive ? 'bg-primary-100' : 'bg-gray-100'
                )}>
                  <feature.icon className={cn(
                    'w-5 h-5',
                    isActive ? 'text-primary-600' : 'text-gray-600'
                  )} />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="font-medium text-gray-900">{feature.name}</h3>
                    {feature.popular && (
                      <span className="px-2 py-0.5 bg-filipino-yellow text-xs font-medium rounded-full">
                        Popular
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500">{feature.description}</p>
                </div>
              </div>
            </Link>
          )
        })}
      </div>

      {/* Feature Content */}
      {children}
    </div>
  )
}