import openai
import json
import time
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from .models import AIModel, AIRequest, AITemplate, AIUsageQuota

class OpenRouterService:
    """Main AI service using OpenRouter for multiple model access"""
    
    def __init__(self, user=None):
        self.user = user
        self.client = openai.OpenAI(
            base_url=getattr(settings, 'OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
            api_key=getattr(settings, 'OPENROUTER_API_KEY', ''),
        )
        
    def get_available_model(self, user_subscription_tier: str, model_type: str = 'chat') -> Optional[AIModel]:
        """Get best available model for user's subscription tier"""
        
        # Model priority based on subscription
        model_priorities = {
            'starter': ['deepseek/deepseek-r1', 'meta-llama/llama-3.2-3b-instruct:free'],
            'business': ['openai/gpt-4o-mini', 'anthropic/claude-3.5-haiku'],
            'pro': ['anthropic/claude-3.5-sonnet', 'openai/gpt-4o', 'deepseek/deepseek-r1']
        }
        
        preferred_models = model_priorities.get(user_subscription_tier, model_priorities['starter'])
        
        # Find best available model
        for model_id in preferred_models:
            try:
                model = AIModel.objects.get(
                    model_id=model_id,
                    model_type=model_type,
                    is_active=True
                )
                return model
            except AIModel.DoesNotExist:
                continue
        
        # Fallback to any available model
        return AIModel.objects.filter(
            model_type=model_type,
            is_active=True,
            min_subscription_tier__in=['starter', user_subscription_tier]
        ).first()
    
    def check_usage_quota(self, user) -> Dict[str, Any]:
        """Check if user has available AI quota"""
        from datetime import datetime
        
        # Get current month quota
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(seconds=1)
        
        quota, created = AIUsageQuota.objects.get_or_create(
            user=user,
            period_type='monthly',
            period_start=month_start,
            defaults={
                'period_end': month_end,
                'max_requests': user.ai_usage_limit,
                'max_tokens': user.ai_usage_limit * 1000,  # Rough estimate
                'max_cost_usd': Decimal('10.00') if user.subscription_tier == 'starter' else Decimal('50.00'),
            }
        )
        
        return {
            'can_use': not quota.is_exceeded and quota.current_requests < quota.max_requests,
            'requests_remaining': max(0, quota.max_requests - quota.current_requests),
            'requests_percentage': quota.requests_percentage,
            'quota': quota
        }
    
    def process_email_to_task(self, email_content: str, user_context: Dict = None) -> Dict[str, Any]:
        """Convert email to actionable task - core AIyos feature"""
        
        if not self.user:
            raise ValueError("User required for AI processing")
        
        # Check quota
        quota_check = self.check_usage_quota(self.user)
        if not quota_check['can_use']:
            raise Exception("AI usage quota exceeded")
        
        # Get appropriate model
        model = self.get_available_model(self.user.subscription_tier)
        if not model:
            raise Exception("No AI model available for your subscription")
        
        # Get business context
        business_context = self._get_business_context(user_context or {})
        
        # Create AI request record
        ai_request = AIRequest.objects.create(
            user=self.user,
            model=model,
            request_type='email_to_task',
            status='processing',
            input_data={
                'email_content': email_content,
                'user_context': user_context,
                'business_context': business_context
            }
        )
        
        try:
            # Prepare prompt with Filipino context
            system_prompt = self._get_filipino_system_prompt('email_to_task')
            user_prompt = self._build_email_to_task_prompt(email_content, business_context)
            
            ai_request.processed_input = f"System: {system_prompt}\n\nUser: {user_prompt}"
            ai_request.save()
            
            start_time = time.time()
            
            # Make API request
            response = self.client.chat.completions.create(
                model=model.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            # Process response
            result = json.loads(response.choices[0].message.content)
            
            # Update request record
            ai_request.status = 'completed'
            ai_request.output_data = result
            ai_request.input_tokens = response.usage.prompt_tokens
            ai_request.output_tokens = response.usage.completion_tokens
            ai_request.total_tokens = response.usage.total_tokens
            ai_request.response_time_ms = response_time_ms
            ai_request.completed_at = timezone.now()
            
            # Calculate cost
            cost_usd = self._calculate_cost(model, response.usage.prompt_tokens, response.usage.completion_tokens)
            ai_request.cost_usd = cost_usd
            ai_request.cost_php = cost_usd * Decimal('56.0')  # Rough PHP conversion
            
            ai_request.save()
            
            # Update user's monthly AI calls
            self.user.monthly_ai_calls += 1
            self.user.save(update_fields=['monthly_ai_calls'])
            
            # Update quota
            quota_check['quota'].update_usage(
                requests=1,
                tokens=response.usage.total_tokens,
                cost_usd=float(cost_usd)
            )
            
            return {
                'success': True,
                'task': result,
                'request_id': ai_request.id,
                'cost_php': ai_request.cost_php,
                'tokens_used': ai_request.total_tokens
            }
            
        except Exception as e:
            # Update request with error
            ai_request.status = 'failed'
            ai_request.error_message = str(e)
            ai_request.completed_at = timezone.now()
            ai_request.save()
            
            return {
                'success': False,
                'error': str(e),
                'request_id': ai_request.id
            }
    
    def generate_filipino_social_content(self, business_update: str, platform: str = 'facebook', user_context: Dict = None) -> Dict[str, Any]:
        """Generate culturally-appropriate social media content for Filipino market"""
        
        if not self.user:
            raise ValueError("User required for AI processing")
        
        # Check quota
        quota_check = self.check_usage_quota(self.user)
        if not quota_check['can_use']:
            raise Exception("AI usage quota exceeded")
        
        model = self.get_available_model(self.user.subscription_tier)
        if not model:
            raise Exception("No AI model available")
        
        # Platform-specific guidelines
        platform_styles = {
            'facebook': 'Casual, engaging, family-oriented, mix English and Tagalog naturally. Include emojis and hashtags.',
            'instagram': 'Visual-focused, aspirational, trending hashtags, younger Filipino audience.',
            'tiktok': 'Fun, trendy, viral potential, Gen Z Filipino slang, catchy and energetic.'
        }
        
        business_context = self._get_business_context(user_context or {})
        
        # Create AI request
        ai_request = AIRequest.objects.create(
            user=self.user,
            model=model,
            request_type='content_generation',
            status='processing',
            input_data={
                'business_update': business_update,
                'platform': platform,
                'user_context': user_context,
                'business_context': business_context
            }
        )
        
        try:
            system_prompt = f"""You are a Filipino social media content creator for SMBs. 
            Create {platform} posts that resonate with Filipino culture and business practices.
            
            Style for {platform}: {platform_styles.get(platform, 'General Filipino business style')}
            
            Guidelines:
            - Mix English and Tagalog naturally (code-switching)
            - Include relevant Filipino culture references
            - Consider Philippine business hours and customs
            - Make it authentic to Filipino SMB voice
            - Include appropriate hashtags
            - Return response as JSON with 'content' and 'hashtags' fields
            """
            
            user_prompt = f"""
            Business: {business_context.get('company_name', 'Filipino Business')}
            Industry: {business_context.get('business_type', 'General')}
            
            Business Update: {business_update}
            
            Create an engaging {platform} post for this update.
            """
            
            ai_request.processed_input = f"System: {system_prompt}\n\nUser: {user_prompt}"
            ai_request.save()
            
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=model.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            result = json.loads(response.choices[0].message.content)
            
            # Update request record
            ai_request.status = 'completed'
            ai_request.output_data = result
            ai_request.input_tokens = response.usage.prompt_tokens
            ai_request.output_tokens = response.usage.completion_tokens
            ai_request.total_tokens = response.usage.total_tokens
            ai_request.response_time_ms = response_time_ms
            ai_request.completed_at = timezone.now()
            
            cost_usd = self._calculate_cost(model, response.usage.prompt_tokens, response.usage.completion_tokens)
            ai_request.cost_usd = cost_usd
            ai_request.cost_php = cost_usd * Decimal('56.0')
            
            ai_request.save()
            
            # Update usage tracking
            self.user.monthly_ai_calls += 1
            self.user.save(update_fields=['monthly_ai_calls'])
            
            quota_check['quota'].update_usage(
                requests=1,
                tokens=response.usage.total_tokens,
                cost_usd=float(cost_usd)
            )
            
            return {
                'success': True,
                'content': result,
                'request_id': ai_request.id,
                'cost_php': ai_request.cost_php,
                'tokens_used': ai_request.total_tokens
            }
            
        except Exception as e:
            ai_request.status = 'failed'
            ai_request.error_message = str(e)
            ai_request.completed_at = timezone.now()
            ai_request.save()
            
            return {
                'success': False,
                'error': str(e),
                'request_id': ai_request.id
            }
    
    def _get_business_context(self, user_context: Dict) -> Dict[str, Any]:
        """Get comprehensive business context for AI processing"""
        context = {
            'company_name': self.user.company_name,
            'business_type': self.user.business_type,
            'preferred_language': self.user.preferred_language,
            'subscription_tier': self.user.subscription_tier,
            'timezone': 'Asia/Manila'
        }
        
        # Add business profile if available
        if hasattr(self.user, 'business_profile'):
            profile = self.user.business_profile
            context.update({
                'industry': profile.industry,
                'employee_count': profile.employee_count,
                'city': profile.city,
                'region': profile.region,
                'business_hours': f"{profile.business_start_time} - {profile.business_end_time}",
                'business_description': profile.business_description,
                'automation_goals': profile.automation_goals
            })
        
        # Merge with provided context
        context.update(user_context)
        return context
    
    def _get_filipino_system_prompt(self, task_type: str) -> str:
        """Get Filipino-contextualized system prompts"""
        
        base_context = """You are an AI assistant specifically designed for Filipino small and medium businesses (SMBs). 
        You understand Philippine business culture, practices, and the unique challenges Filipino entrepreneurs face.
        
        Key Filipino Business Context:
        - Business hours typically 9 AM - 6 PM (PHT)
        - English and Tagalog code-switching is natural
        - Relationship-based business culture ("pakikipagkapwa")
        - Family-oriented business values
        - Cost-conscious decision making
        - Government compliance requirements (BIR, DTI, SSS, PhilHealth)
        - Common challenges: cash flow, competition, technology adoption
        """
        
        task_prompts = {
            'email_to_task': base_context + """
            Your task is to convert emails into clear, actionable tasks for Filipino business owners.
            Consider Philippine business customs, holidays, and working schedules.
            
            Output format (JSON):
            {
                "title": "Clear task title",
                "description": "Detailed description",
                "priority": 1-5 (1=highest),
                "due_date": "YYYY-MM-DD or 'asap' or 'flexible'",
                "category": "email, meeting, payment, compliance, etc.",
                "estimated_duration": "time in minutes",
                "required_actions": ["action 1", "action 2"],
                "filipino_context": "any specific Filipino business considerations"
            }
            """,
            
            'content_generation': base_context + """
            Create social media content that resonates with Filipino audiences.
            Use natural English-Tagalog code-switching and Filipino cultural references.
            """
        }
        
        return task_prompts.get(task_type, base_context)
    
    def _build_email_to_task_prompt(self, email_content: str, business_context: Dict) -> str:
        """Build contextual prompt for email-to-task conversion"""
        
        prompt = f"""
        Please convert this email into an actionable task for my Filipino business.
        
        Business Context:
        - Company: {business_context.get('company_name', 'N/A')}
        - Industry: {business_context.get('business_type', 'N/A')}
        - Location: {business_context.get('city', 'Philippines')}
        
        Email Content:
        {email_content}
        
        Consider:
        - Philippine business hours and customs
        - Urgency level appropriate for Filipino business pace
        - Any government compliance requirements
        - Cost considerations for SMB
        
        Return a JSON object with the task details.
        """
        
        return prompt
    
    def _calculate_cost(self, model: AIModel, input_tokens: int, output_tokens: int) -> Decimal:
        """Calculate cost for AI request"""
        input_cost = Decimal(str(model.provider.cost_per_input_token)) * input_tokens
        output_cost = Decimal(str(model.provider.cost_per_output_token)) * output_tokens
        return input_cost + output_cost

# Convenience function for easy access
def get_ai_service(user=None) -> OpenRouterService:
    """Get configured AI service instance"""
    return OpenRouterService(user=user)