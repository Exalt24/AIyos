'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'react-hot-toast'
import { 
  MegaphoneIcon,
  HashtagIcon,
  HeartIcon,
  ShareIcon
} from '@heroicons/react/24/outline'
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { aiService } from '@/services/ai'
import { SOCIAL_PLATFORMS, CONTENT_TONES } from '@/lib/constants'
import { formatCurrency } from '@/lib/utils'

const socialContentSchema = z.object({
  business_update: z.string().min(5, 'Business update must be at least 5 characters'),
  platform: z.enum(['facebook', 'instagram', 'tiktok', 'linkedin']),
  tone: z.enum(['professional', 'casual', 'friendly', 'excited']),
  include_hashtags: z.boolean(),
  include_call_to_action: z.boolean(),
  target_audience: z.string().optional(),
})

type SocialContentForm = z.infer<typeof socialContentSchema>

interface ContentResult {
  content: string
  hashtags: string[]
  call_to_action?: string
  engagement_tips?: string[]
}

export default function SocialContentPage() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState<ContentResult | null>(null)
  const [generationInfo, setGenerationInfo] = useState<{
    cost_php: number
    tokens_used: number
    request_id: string
  } | null>(null)

  // Properly typed useForm with explicit generic
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue
  } = useForm<SocialContentForm>({
    resolver: zodResolver(socialContentSchema),
    defaultValues: {
      platform: 'facebook',
      tone: 'friendly',
      include_hashtags: true, // Set defaults here instead of in schema
      include_call_to_action: true,
      target_audience: '', // Initialize as empty string instead of undefined
    }
  })

  const selectedPlatform = watch('platform')
  const businessUpdate = watch('business_update', '')

  const onSubmit = async (data: SocialContentForm) => {
    setIsGenerating(true)
    setResult(null)
    setGenerationInfo(null)

    try {
      const response = await aiService.generateSocialContent(data)
      
      if (response.success) {
        setResult(response.content)
        setGenerationInfo({
          cost_php: response.cost_php,
          tokens_used: response.tokens_used,
          request_id: response.request_id
        })
        toast.success('Social content generated successfully! 🎉')
      } else {
        toast.error(response.error || 'Failed to generate content')
      }
    } catch (error: any) {
      console.error('Content generation error:', error)
      toast.error(error.response?.data?.error || 'Failed to generate content')
    } finally {
      setIsGenerating(false)
    }
  }

  const getPlatformIcon = (platform: string) => {
    const platformData = SOCIAL_PLATFORMS.find(p => p.value === platform)
    return platformData?.icon || '📱'
  }

  const getPlatformColor = (platform: string) => {
    const platformData = SOCIAL_PLATFORMS.find(p => p.value === platform)
    return platformData?.color || 'text-gray-600'
  }

  const copyToClipboard = async () => {
    if (!result) return
    
    let contentToCopy = result.content
    
    if (result.hashtags && result.hashtags.length > 0) {
      contentToCopy += '\n\n' + result.hashtags.map(tag => `#${tag}`).join(' ')
    }
    
    if (result.call_to_action) {
      contentToCopy += '\n\n' + result.call_to_action
    }
    
    try {
      await navigator.clipboard.writeText(contentToCopy)
      toast.success('Content copied to clipboard!')
    } catch (error) {
      toast.error('Failed to copy content')
    }
  }

  return (
    <div className="space-y-6">
      {/* Feature Description */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MegaphoneIcon className="w-6 h-6 text-primary-600 mr-2" />
            Filipino Social Media Content Generator
          </CardTitle>
          <CardDescription>
            Generate engaging social media content na perfect para sa Filipino audience. 
            Natural na English-Tagalog mix with cultural context.
          </CardDescription>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Content Details</CardTitle>
            <CardDescription>
              Tell us about your business update and we'll create engaging social content
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Business Update *
                </label>
                <textarea
                  {...register('business_update')}
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  placeholder="What's happening with your business?

Examples:
- Opened new branch in Makati
- Launched new product line
- Hiring new employees
- Special promotion this month
- Anniversary celebration
- New partnership announcement"
                />
                {errors.business_update && (
                  <p className="mt-1 text-sm text-red-600">{errors.business_update.message}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  {businessUpdate.length} characters
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Platform
                  </label>
                  <div className="space-y-2">
                    {SOCIAL_PLATFORMS.map((platform) => (
                      <label
                        key={platform.value}
                        className="flex items-center space-x-2 cursor-pointer"
                      >
                        <input
                          {...register('platform')}
                          type="radio"
                          value={platform.value}
                          className="text-primary-600 focus:ring-primary-500"
                        />
                        <span className={`text-lg ${platform.color}`}>
                          {platform.icon}
                        </span>
                        <span className="text-sm text-gray-700">{platform.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tone
                  </label>
                  <select
                    {...register('tone')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {CONTENT_TONES.map((tone) => (
                      <option key={tone.value} value={tone.value}>
                        {tone.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target Audience (Optional)
                </label>
                <input
                  {...register('target_audience')}
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="e.g., Young professionals, Parents, Small business owners"
                />
              </div>

              <div className="space-y-3">
                <label className="flex items-center space-x-2">
                  <input
                    {...register('include_hashtags')}
                    type="checkbox"
                    className="text-primary-600 focus:ring-primary-500 rounded"
                  />
                  <span className="text-sm text-gray-700">Include hashtags</span>
                </label>
                
                <label className="flex items-center space-x-2">
                  <input
                    {...register('include_call_to_action')}
                    type="checkbox"
                    className="text-primary-600 focus:ring-primary-500 rounded"
                  />
                  <span className="text-sm text-gray-700">Include call-to-action</span>
                </label>
              </div>

              <Button
                type="submit"
                className="w-full"
                isLoading={isGenerating}
                disabled={isGenerating || !businessUpdate.trim()}
              >
                {isGenerating ? 'Generating Content...' : 'Generate Social Post'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Result Display */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <span className={`text-2xl mr-2 ${getPlatformColor(selectedPlatform)}`}>
                {getPlatformIcon(selectedPlatform)}
              </span>
              Generated Content
            </CardTitle>
            <CardDescription>
              {result ? 'Your AI-generated social media post' : 'Content will appear here after generation'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isGenerating && (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
                  <p className="text-gray-600">Generating Filipino social content...</p>
                  <p className="text-sm text-gray-500 mt-1">Creating culturally relevant content</p>
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* Post Content */}
                <div className="bg-gray-50 rounded-lg p-4 border">
                  <div className="whitespace-pre-wrap text-gray-900 leading-relaxed">
                    {result.content}
                  </div>
                </div>

                {/* Hashtags */}
                {result.hashtags && result.hashtags.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <HashtagIcon className="w-4 h-4 mr-1" />
                      Hashtags
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {result.hashtags.map((hashtag, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm font-medium"
                        >
                          #{hashtag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Call to Action */}
                {result.call_to_action && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Call to Action</h4>
                    <p className="text-gray-700 text-sm bg-green-50 border border-green-200 rounded-lg p-3">
                      {result.call_to_action}
                    </p>
                  </div>
                )}

                {/* Engagement Tips */}
                {result.engagement_tips && result.engagement_tips.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                      <HeartIcon className="w-4 h-4 mr-1" />
                      Engagement Tips
                    </h4>
                    <ul className="space-y-1">
                      {result.engagement_tips.map((tip, index) => (
                        <li key={index} className="flex items-start text-sm text-gray-700">
                          <span className="text-primary-600 mr-2">•</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Processing Info */}
                {generationInfo && (
                  <div className="border-t border-gray-200 pt-4">
                    <div className="flex justify-between items-center text-sm text-gray-600">
                      <span>Generation Cost:</span>
                      <span className="font-medium">{formatCurrency(generationInfo.cost_php)}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm text-gray-600">
                      <span>Tokens Used:</span>
                      <span className="font-medium">{generationInfo.tokens_used.toLocaleString()}</span>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-3 pt-4">
                  <Button 
                    size="sm" 
                    className="flex-1"
                    onClick={copyToClipboard}
                  >
                    <ShareIcon className="w-4 h-4 mr-1" />
                    Copy to Clipboard
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    Save as Template
                  </Button>
                </div>
              </div>
            )}

            {!result && !isGenerating && (
              <div className="text-center py-12 text-gray-500">
                <MegaphoneIcon className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>Enter your business update and generate engaging social content</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Platform-specific Tips */}
      <Card>
        <CardHeader>
          <CardTitle>Platform Best Practices</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                📘 Facebook
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Family-oriented messaging</li>
                <li>• Mix English & Tagalog</li>
                <li>• Community building focus</li>
                <li>• Story-driven content</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                📷 Instagram
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Visual-first approach</li>
                <li>• Aspirational content</li>
                <li>• Trending hashtags</li>
                <li>• Stories integration</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                🎵 TikTok
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Fun & energetic tone</li>
                <li>• Gen Z Filipino slang</li>
                <li>• Viral potential focus</li>
                <li>• Short & catchy</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                💼 LinkedIn
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Professional tone</li>
                <li>• Business insights</li>
                <li>• Industry relevance</li>
                <li>• Thought leadership</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}