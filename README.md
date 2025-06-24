# AIyos - AI Automation SaaS for Filipino Businesses

🚀 **PROJECT STATUS: CODE COMPLETE - TESTING & DEBUGGING PHASE**

AIyos is a comprehensive AI-powered automation platform specifically designed for Filipino small and medium businesses (SMBs). Built with Django REST API backend and Next.js TypeScript frontend, it provides intelligent workflow automation with deep Filipino business context.

## 🌟 Key Features

- **🤖 AI-Powered Email-to-Task Automation** - Convert emails into actionable tasks with Filipino context understanding
- **📱 Social Content Generation** - Create platform-specific content with English-Tagalog code-switching
- **🏦 Local Payment Integration** - GCash, PayMaya, BPI, and other Philippine financial services
- **🔄 Workflow Automation Engine** - Visual workflow builder with Filipino business templates
- **💰 Cost-Effective AI** - Progressive model scaling (DeepSeek R1 → GPT-4o-mini → Claude 3.5)
- **🇵🇭 Filipino-First Design** - Tagalog support, PHP pricing, Asia/Manila timezone, local business types

## 🏗️ Tech Stack

### Backend (Django REST API)

- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Cache & Jobs**: Redis + Celery
- **AI Integration**: OpenRouter with multiple model support
- **Authentication**: JWT with SimpleJWT
- **Documentation**: DRF Spectacular (OpenAPI/Swagger)

### Frontend (Next.js)

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Headless UI
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts
- **Icons**: Heroicons + Lucide React

### Deployment

- **Backend**: Render (Docker + PostgreSQL + Redis)
- **Frontend**: Vercel (Global CDN + Edge Functions)
- **Infrastructure Cost**: $14-201/month (bootstrap-optimized)

## 📋 Prerequisites

### Required Software

- **Node.js** 18+ with npm/yarn
- **Python** 3.11+
- **PostgreSQL** 15+ (or SQLite for development)
- **Redis** 6+ (for production/full testing)
- **Git** for version control

### Required API Keys

- **OpenRouter API Key** - For AI features (get from [openrouter.ai](https://openrouter.ai))
- **Stripe API Keys** - For subscription payments (optional for development)

### Verify Prerequisites

```bash
node --version    # Should show v18+ 
python --version  # Should show 3.11+ (Windows)
python3 --version # Should show 3.11+ (Linux/Mac)
git --version     # Any recent version
```

## 🚀 Complete Setup Guide

### Step 1: Clone and Install Root Dependencies

```bash
git clone https://github.com/Exalt24/AIyos.git
cd AIyos

# Install concurrently (required for running both servers)
npm install
```

### Step 2: Backend Setup

<details>
<summary><strong>🪟 Windows Backend Setup</strong></summary>

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment  
venv\Scripts\activate

# You should see (venv) in your command prompt
# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Backend Setup</strong></summary>

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

</details>

### Step 3: Generate Required Keys

**Before configuring the environment, you need to generate secure keys:**

#### Generate Django SECRET_KEY

```bash
# Ensure you're in backend directory with virtual environment activated
cd backend
venv\Scripts\activate           # Windows
source venv/bin/activate        # Linux/Mac

# Generate a secure Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example Output:**
```
django-insecure-8k2@9j_m4!q7p#r*v+n8w@3s%7c$e9u&2i1o#k6f4g*h5j-x7z
```

**Copy this generated key** - you'll use it in the next step.

#### Get OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

### Step 4: Configure Backend Environment

**Critical:** Edit `backend/.env` with your **generated values** (not placeholders):

```env
# Django Core Settings (replace with YOUR generated secret key)
SECRET_KEY=django-insecure-dev-key-change-in-production-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Redis Configuration (for Celery and Cache)
REDIS_URL=redis://localhost:6379

# AI Integration (REQUIRED - Replace with your actual OpenRouter API key)
OPENROUTER_API_KEY=sk-or-v1-your-actual-openrouter-api-key-here
CURRENT_AI_MODEL=deepseek/deepseek-r1

# File Storage (Optional for development - leave empty or use real values)
CLOUDINARY_URL=

# Email Backend (Development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security and CORS
CORS_ORIGIN_WHITELIST=http://localhost:3000,https://aiyos.vercel.app

# Optional: Stripe Settings (leave empty for development)
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Optional: Additional Django Settings
DJANGO_SETTINGS_MODULE=aiyos.settings
PYTHONPATH=/app
```

**⚠️ Critical Steps:** 
1. **Replace SECRET_KEY** with the key you generated in Step 3
2. **Replace OPENROUTER_API_KEY** with your real API key from OpenRouter
3. **No spaces around the `=` sign**
4. **No quotes around values unless specified**

**Example of what your actual .env should look like:**
```env
SECRET_KEY=django-insecure-8k2@9j_m4!q7p#r*v+n8w@3s%7c$e9u&2i1o#k6f4g*h5j-x7z
OPENROUTER_API_KEY=sk-or-v1-1234567890abcdef1234567890abcdef1234567890abcdef
# ... rest of the configuration
```

### Step 5: Frontend Setup

```bash
# Navigate to frontend (from root directory)
cd frontend

# Install Node.js dependencies
npm install

# Copy environment template
cp .env.local.example .env.local    # Linux/Mac
copy .env.local.example .env.local  # Windows
```

### Step 6: Configure Frontend Environment

Edit `frontend/.env.local` with these **exact** values:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# App Configuration
NEXT_PUBLIC_APP_NAME=AIyos
NEXT_PUBLIC_ENABLE_FILIPINO_LANG=true

# Optional: Analytics (leave empty for development)
NEXT_PUBLIC_GA_ID=
```

### Step 7: Database Setup

```bash
# Navigate back to backend (from frontend directory)
cd ../backend

# Ensure virtual environment is activated (you should see (venv) in prompt)
# If not activated:
venv\Scripts\activate           # Windows
source venv/bin/activate        # Linux/Mac

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create Django admin user
python manage.py createsuperuser
```

**Superuser Creation Prompts:**
- Username: `admin` (or your preference)
- Email: `your-email@example.com`
- Password: Choose a secure password (8+ characters)

### Step 8: Verify Complete Setup

```bash
# Navigate back to root directory
cd ..

# Run environment check - should show ALL GREEN ✅
node scripts/check-env.js
```

**Expected Output:** All items should show green ✅ checkmarks. If you see red ❌, review the steps above.

## 🏃 Running the Application

### Method 1: Start Both Servers Together (Recommended)

```bash
# From root directory, ensure virtual environment paths are correct
npm run dev              # Windows (default)
npm run dev:unix         # Linux/Mac
```

### Method 2: Start Servers Individually

<details>
<summary><strong>🪟 Windows Individual Startup</strong></summary>

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python manage.py runserver 8000

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Individual Startup</strong></summary>

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python3 manage.py runserver 8000

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
```

</details>

## 🌐 Application URLs

Once both servers are running successfully:

- **🎯 Frontend Application**: `http://localhost:3000`
- **🔧 Backend API**: `http://localhost:8000/api`
- **👤 Django Admin**: `http://localhost:8000/admin`
- **📚 API Documentation**: `http://localhost:8000/api/docs`

## 🔧 Essential Development Commands

```bash
# 🚀 Start development (with virtual environment activation)
npm run dev              # Windows default
npm run dev:unix         # Linux/Mac

# 🔍 Check environment setup (run this first if issues)
npm run check:env

# 🧹 Clean cache and build files  
npm run clean

# 🏃 Run servers individually
npm run backend:dev      # Django only (Windows)
npm run backend:dev:unix # Django only (Linux/Mac)
npm run frontend:dev     # Next.js only (all platforms)

# 👤 Create additional admin users
npm run backend:superuser      # Windows
npm run backend:superuser:unix # Linux/Mac

# 🗄️ Database operations
npm run backend:migrate        # Apply database changes
npm run backend:makemigrations # Create new migrations

# 📊 Run tests
npm run test

# 🏗️ Build for production
npm run build
```

## 🔧 Troubleshooting Common Issues

### Environment Check Failures

**Problem:** Red ❌ marks in environment check

1. **Missing environment files:**
   ```bash
   # Ensure these files exist with actual values:
   ls backend/.env
   ls frontend/.env.local
   ```

2. **Placeholder values still present:**
   ```bash
   # Check for placeholder values in backend/.env:
   grep "your_" backend/.env
   # Should return nothing
   
   # Check for placeholder SECRET_KEY:
   grep "your-super-secret-key" backend/.env
   # Should return nothing
   ```

3. **Virtual environment not found:**
   ```bash
   cd backend
   # Recreate if needed:
   rm -rf venv
   python -m venv venv          # Windows
   python3 -m venv venv         # Linux/Mac
   ```

### SECRET_KEY Generation Issues

**Problem:** Can't generate SECRET_KEY or getting errors

**Solution 1: Use Django's generator (Recommended)**
```bash
cd backend
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Solution 2: Use online generator**
- Visit [djecrety.ir](https://djecrety.ir/)
- Click "Generate" button
- Copy the generated key

**Solution 3: Manual generation**
```python
# If Django import fails, use this:
import secrets
import string
chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
key = ''.join(secrets.choice(chars) for _ in range(50))
print(f"django-insecure-{key}")
```

**Problem:** SECRET_KEY still shows as placeholder in environment check

1. **Verify the key was properly saved:**
   ```bash
   grep SECRET_KEY backend/.env
   # Should show your actual generated key, not placeholder
   ```

2. **Ensure no extra characters:**
   ```bash
   # Key should be on one line with no quotes:
   SECRET_KEY=django-insecure-your-actual-generated-key-here
   ```

### Virtual Environment Issues

**Windows activation problems:**
```bash
cd backend
# Try these alternatives:
venv\Scripts\activate
venv\Scripts\activate.bat
venv\Scripts\Activate.ps1

# If PowerShell execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac activation problems:**
```bash
cd backend
# Check permissions:
chmod +x venv/bin/activate
source venv/bin/activate

# Verify activation:
which python  # Should show path to venv/bin/python
```

### Module Import Errors

**Python packages not found:**
```bash
cd backend
# Ensure virtual environment is activated (see (venv) in prompt)
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

# Reinstall dependencies:
pip install --upgrade pip
pip install -r requirements.txt

# Test Django installation:
python -c "import django; print(django.get_version())"
```

**Node.js dependency issues:**
```bash
cd frontend
# Clear and reinstall:
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules & del package-lock.json  # Windows
npm install

# Verify Next.js:
npx next --version
```

### Database Issues

**Migration errors:**
```bash
cd backend
source venv/bin/activate  # Ensure venv is active

# Check migration status:
python manage.py showmigrations

# Create fresh migrations:
python manage.py makemigrations --empty authentication
python manage.py makemigrations --empty automations
python manage.py makemigrations --empty integrations
python manage.py makemigrations --empty ai_services
python manage.py migrate
```

**Database locked error:**
```bash
# Stop all Django processes first, then:
cd backend
rm db.sqlite3  # This removes the database
python manage.py migrate
python manage.py createsuperuser
```

### Port Conflicts

**Ports 3000 or 8000 already in use:**

Windows:
```bash
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

Linux/Mac:
```bash
# Kill processes on ports:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or use different ports:
# Backend: python manage.py runserver 8001
# Frontend: npm run dev -- -p 3001
```

### API Connection Issues

**Frontend can't reach backend:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/api/
   # Should return JSON response
   ```

2. **Check CORS settings in backend/.env:**
   ```env
   CORS_ORIGIN_WHITELIST=http://localhost:3000
   ```

3. **Verify frontend environment:**
   ```bash
   grep NEXT_PUBLIC_API_URL frontend/.env.local
   # Should show: NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

### AI Features Not Working

**OpenRouter API integration issues:**

1. **Verify API key in backend/.env:**
   ```bash
   grep OPENROUTER_API_KEY backend/.env
   # Should show your actual API key, not placeholder
   ```

2. **Test API key validity:**
   ```bash
   curl -H "Authorization: Bearer your-api-key" https://openrouter.ai/api/v1/models
   ```

3. **Check model availability:**
   ```env
   # In backend/.env:
   CURRENT_AI_MODEL=deepseek/deepseek-r1
   ```

## 📁 Project Structure

```
AIyos/
├── backend/                    # Django REST API
│   ├── authentication/         # User auth + business profiles
│   ├── automations/            # Workflow engine
│   ├── integrations/           # Filipino service integrations
│   ├── ai_services/            # OpenRouter AI integration
│   ├── aiyos/                  # Django project config
│   ├── venv/                   # Python virtual environment
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Backend environment variables
│   ├── db.sqlite3             # SQLite database (after setup)
│   └── manage.py              # Django management
│
├── frontend/                   # Next.js TypeScript app
│   ├── src/
│   │   ├── app/               # Next.js 14 app router
│   │   ├── components/        # Reusable UI components
│   │   ├── services/          # API service layer
│   │   ├── store/             # Zustand state management
│   │   ├── types/             # TypeScript definitions
│   │   └── lib/               # Utilities & constants
│   ├── node_modules/          # Node dependencies (after npm install)
│   ├── package.json           # Node dependencies
│   ├── .env.local             # Frontend environment variables
│   └── next.config.ts         # Next.js configuration
│
├── scripts/                    # Development utilities
│   └── check-env.js           # Environment validation script
├── package.json               # Root package.json with concurrently
├── .gitignore                 # Comprehensive gitignore
└── README.md                  # This file
```

## 🧪 Testing Your Setup

### 1. Environment Validation

```bash
# This should show ALL GREEN ✅
node scripts/check-env.js
```

**Common issues if not all green:**
- Missing SECRET_KEY: Generate using Django's method in Step 3
- Missing OpenRouter API key: Get from openrouter.ai
- Placeholder values: Replace with actual generated values

### 2. Backend API Test

```bash
# Test basic API endpoint
curl http://localhost:8000/api/
# Expected: JSON response with API information

# Test Django admin
# Visit: http://localhost:8000/admin
# Login with superuser credentials
```

### 3. Frontend Application Test

1. Open http://localhost:3000
2. Check browser console for errors (F12 → Console)
3. Try registering a new account
4. Navigate between pages
5. Test responsive design (mobile view)

### 4. AI Integration Test (If API Key Configured)

1. Register/login to the application
2. Navigate to AI features section
3. Test Email-to-Task converter with sample content:
   ```
   Subject: Team Meeting Next Week
   Content: Hi team, we need to schedule our quarterly review meeting for next Tuesday at 2 PM. Please prepare your project updates and bring quarterly reports. Location will be Conference Room A.
   ```
4. Test Social Content Generator with sample input:
   ```
   Business Update: "Launching new delivery service in Makati"
   Platform: Facebook
   Tone: Excited
   ```

## 💰 Subscription Tiers

- **Starter**: ₱1,500/month (~$27) - 1,000 AI calls, basic automations
- **Business**: ₱4,200/month (~$75) - 5,000 AI calls, premium integrations  
- **Pro**: ₱8,400/month (~$150) - Unlimited AI calls, custom features

## 🇵🇭 Filipino Market Features

### Language Support

- **Mixed Language Processing**: English-Tagalog code-switching
- **Cultural Context**: Filipino business hours, local terminology
- **Time-based Tagalog Greetings**: "Magandang umaga", "Magandang hapon"

### Local Integrations

- **Payment Services**: GCash, PayMaya, GrabPay, Philippine banks
- **E-commerce**: Shopee, Lazada APIs
- **Government**: BIR, DTI, SSS compliance automation
- **Social Media**: Facebook Business, TikTok for Business

### Business Templates

- **BPO Companies**: HR workflows, client communication
- **Real Estate**: Property management, client follow-ups
- **E-commerce**: Order processing, inventory management
- **OFW Families**: Remittance tracking, financial planning

## 🚀 Deployment

### Staging Deployment (Weeks 5-6)

- **Backend**: Render staging environment
- **Frontend**: Vercel preview deployment  
- **Database**: Render PostgreSQL
- **Environment**: Staging API keys and configuration

### Production Deployment (Weeks 7-8)

- **Domain**: AIyos.ph (tentative) registration
- **Backend**: Render production with managed PostgreSQL + Redis
- **Frontend**: Vercel production with custom domain
- **Monitoring**: Error tracking and performance monitoring
- **Security**: SSL, rate limiting, input validation

## 🤝 Contributing

### Development Process

1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Test Locally**: Run both backend and frontend servers
3. **Test Integration**: Verify API endpoints and UI components
4. **Create Pull Request**: Include testing checklist and screenshots
5. **Code Review**: Team review before merging to main

### Code Standards

- **Backend**: Follow Django best practices, PEP 8 formatting
- **Frontend**: TypeScript strict mode, ESLint + Prettier
- **Commits**: Conventional commits format
- **Testing**: Manual testing checklist for each feature

## 📞 Support

### Getting Help

- **Documentation Issues**: Create GitHub issue with `documentation` label
- **Setup Problems**: Check troubleshooting section first, then create issue
- **Feature Questions**: Review project roadmap in documentation
- **Team Communication**: Use project Discord/Slack channel

### Current Development Phase

🔧 **TESTING & DEBUGGING PHASE**

- Priority: Get application running locally with all green checkmarks
- Focus: Fix integration issues and ensure all features work
- Next: Systematic testing before staging deployment

## 🎯 Launch Timeline

- **Weeks 1-2**: Local development setup and core feature testing
- **Weeks 3-4**: Integration testing and bug fixes  
- **Weeks 5-6**: Staging deployment and beta testing
- **Weeks 7-8**: Production launch and first customer onboarding

## 📄 License

This project is proprietary software. All rights reserved.

---

**Made with ❤️ in 🇵🇭 Philippines for Filipino businesses**

For technical questions or setup issues, create an issue in this repository or contact the development team.