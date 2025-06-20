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

- **OpenRouter API Key** - For AI features
- **Stripe API Keys** - For subscription payments (optional for development)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Exalt24/AIyos.git
cd AIyos
```

### 2. One-Command Setup

**Step 1: Install Root Dependencies**

```bash
# Install concurrently (for running both servers)
npm install
```

**Step 2: Complete Project Setup**

<details>
<summary><strong>🪟 Windows Setup</strong></summary>

```bash
# Create and activate Python virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Go back to root and install frontend dependencies
cd ..
cd frontend
npm install

# Return to root directory
cd ..

# Run database migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Create Django admin user
python manage.py createsuperuser

# Return to root directory for development
cd ..
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Setup</strong></summary>

```bash
# Create and activate Python virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Go back to root and install frontend dependencies
cd ../frontend
npm install

# Return to root directory
cd ..

# Run database migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Create Django admin user
python manage.py createsuperuser

# Return to root directory for development
cd ..
```

</details>

**Alternative: Automated Setup**

<details>
<summary><strong>🪟 Windows Automated Setup (Default)</strong></summary>

```bash
# Install root dependencies (concurrently only)
npm install

# Run Windows setup (default)
npm run setup
# OR explicitly:
npm run setup:windows

# Create admin user
npm run backend:superuser
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Automated Setup</strong></summary>

```bash
# Install root dependencies (concurrently only)  
npm install

# Run Unix-specific setup (uses python3)
npm run setup:unix

# Create admin user
npm run backend:superuser:unix
```

</details>

### 3. Configure Environment Variables

**Backend Environment Setup:**

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Navigate to backend and copy environment template
cd backend
copy .env.example .env

# Activate virtual environment to verify setup
venv\Scripts\activate
```

</details>

<details>
<summary><strong>🐧 Linux/Mac</strong></summary>

```bash
# Navigate to backend and copy environment template
cd backend
cp .env.example .env

# Activate virtual environment to verify setup
source venv/bin/activate
```

</details>

**Edit `backend/.env` with your configuration:**

```env
# Django Core
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# AI Integration (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here
CURRENT_AI_MODEL=deepseek/deepseek-r1

# CORS
CORS_ORIGIN_WHITELIST=http://localhost:3000
```

**Frontend Environment Setup:**

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Navigate to frontend
cd ..\frontend
copy .env.local.example .env.local
```

</details>

<details>
<summary><strong>🐧 Linux/Mac</strong></summary>

```bash
# Navigate to frontend  
cd ../frontend
cp .env.local.example .env.local
```

</details>

**Edit `frontend/.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=AIyos
NEXT_PUBLIC_ENABLE_FILIPINO_LANG=true
```

### 4. Start Development

**Quick Start (Windows Default):**

```bash
# Start both servers with virtual environment activation
npm run dev
```

**Platform-Specific Development Commands:**

<details>
<summary><strong>🪟 Windows Development (Default)</strong></summary>

```bash
# Start both servers with virtual environment activation
npm run dev                    # Default Windows mode
npm run dev:windows            # Explicit Windows mode

# Or run individually:
npm run backend:dev            # Django with venv activation (Windows)
npm run frontend:dev           # Next.js (same for all platforms)
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Development</strong></summary>

```bash
# Start both servers with virtual environment activation  
npm run dev:unix

# Or run individually:
npm run backend:dev:unix       # Django with venv activation (Unix)
npm run frontend:dev           # Next.js (same for all platforms)
```

</details>

**Important:** The virtual environment **must be activated** for the Django backend to access installed packages. The commands handle this automatically (Windows by default).

**Development URLs:**

- 🎯 **Frontend**: `http://localhost:3000`
- 🔧 **Backend API**: `http://localhost:8000/api`
- 👤 **Django Admin**: `http://localhost:8000/admin`
- 📚 **API Docs**: `http://localhost:8000/api/docs`

**Cross-Platform Note:** Default commands use Windows syntax. Linux/Mac users should use the `:unix` variants (e.g., `npm run dev:unix`).

## 📁 Project Structure

```
AIyos/
├── backend/                    # Django REST API
│   ├── authentication/         # User auth + business profiles
│   ├── automations/            # Workflow engine
│   ├── integrations/           # Filipino service integrations
│   ├── ai_services/            # OpenRouter AI integration
│   ├── aiyos/                  # Django project config
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Backend environment variables
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
│   ├── package.json           # Node dependencies
│   ├── .env.local             # Frontend environment variables
│   └── next.config.ts         # Next.js configuration
│
├── scripts/                    # Development utilities
│   └── check-env.js           # Environment validation
├── package.json               # Root package.json with concurrently
├── .gitignore                 # Comprehensive gitignore
└── README.md                  # This file
```

## 🔧 Development Workflow

### Essential Commands

```bash
# 🚀 Start development (Windows default, with venv activation)
npm run dev              # Default Windows mode
npm run dev:windows      # Explicit Windows mode  
npm run dev:unix         # For Linux/Mac users

# 🔍 Check environment setup
npm run check:env

# 📦 Install only root dependencies (concurrently)
npm install

# 🧹 Clean cache and build files  
npm run clean

# 🔨 Setup commands
npm run setup            # Default Windows setup
npm run setup:windows    # Explicit Windows setup
npm run setup:unix       # For Linux/Mac

# 🏃 Run servers individually (with venv)
npm run backend:dev      # Django only (Windows default)
npm run backend:dev:unix # Django only (Linux/Mac)
npm run frontend:dev     # Next.js only (all platforms)

# 👤 Create admin user
npm run backend:superuser      # Windows default
npm run backend:superuser:unix # Linux/Mac

# 📊 Run tests
npm run test

# 🏗️ Build for production
npm run build
```

### Environment Check

Before starting development, always run:

```bash
npm run check:env
```

This will verify:

- ✅ Project structure is correct
- ✅ Dependencies are installed
- ✅ Environment variables are configured
- ✅ Database is set up
- ✅ Both servers can start

### Troubleshooting Setup Issues

**Cross-Platform Virtual Environment Issues:**

<details>
<summary><strong>🪟 Windows Common Issues</strong></summary>

```bash
# If venv activation fails
cd backend
python -m venv venv --clear
venv\Scripts\activate.bat

# If pip install fails with permissions
pip install --user -r requirements.txt

# If Python command not found
py -m venv venv
py -m pip install -r requirements.txt
```

</details>

<details>
<summary><strong>🐧 Linux/Mac Common Issues</strong></summary>

```bash
# If python3 command not found (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip python3-venv

# If virtual environment fails
cd backend
python3 -m venv venv --clear
source venv/bin/activate

# If permission denied
sudo chown -R $USER:$USER .
chmod +x venv/bin/activate

# macOS: If python3 not found
brew install python3
```

</details>

**Step-by-Step Manual Setup:**

```bash
# If automated setup fails, try manual approach:

# 1. Root dependencies only (just concurrently)
npm install

# 2. Backend setup manually
cd backend
python -m venv venv                    # Windows
# OR
python3 -m venv venv                   # Linux/Mac

# Activate virtual environment
venv\Scripts\activate                  # Windows  
# OR
source venv/bin/activate               # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# 3. Frontend setup manually
cd ../frontend
npm install

# 4. Database setup
cd ../backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser          # Windows

# OR for Linux/Mac:
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py createsuperuser         # Linux/Mac

# 5. Return to root and test
cd ..
npm run check:env
```

### Testing Checklist

#### 🔧 Phase 1: Local Development Setup

- [ ] Backend Django server running at `localhost:8000`
- [ ] Frontend Next.js server running at `localhost:3000`  
- [ ] Database migrations applied successfully
- [ ] Admin interface accessible with superuser account
- [ ] API documentation loads at `/api/docs/`

#### 🧪 Phase 2: Core Feature Testing

- [ ] User registration with business profile
- [ ] Login/logout flow with JWT tokens
- [ ] Dashboard loads with user stats
- [ ] Email-to-Task AI feature (requires OpenRouter API key)
- [ ] Social Content Generator
- [ ] Navigation between all pages
- [ ] Mobile responsive design

#### 🔗 Phase 3: Integration Testing

- [ ] Frontend-backend API communication
- [ ] Authentication state management
- [ ] Error handling and toast notifications
- [ ] Form validation (React Hook Form + Zod)
- [ ] AI usage tracking and quota management

### Common Issues & Solutions

**Backend Issues:**

```bash
# Database migration errors
python manage.py makemigrations --empty appname
python manage.py migrate --fake

# Module import errors
pip install -r requirements.txt

# Permission errors on Windows
venv\Scripts\activate.bat
```

**Frontend Issues:**

```bash
# Module resolution errors
rm -rf node_modules package-lock.json
npm install

# TypeScript errors
npm run type-check

# Build errors
npm run build
```

## 🧪 Testing Guidelines

### Manual Testing Priority

1. **Authentication Flow**: Register → Login → Dashboard
2. **AI Features**: Test with sample data (email content, social media prompts)
3. **Navigation**: All menu items and page transitions
4. **Responsive Design**: Mobile, tablet, desktop views
5. **Error States**: Network errors, invalid inputs, API failures

### Test Data

Use these sample inputs for testing:

**Email-to-Task Testing:**

```text
Sample Email Content:
"Hi, we need to schedule a client meeting for next week to discuss the Q1 marketing campaign. Please prepare the presentation materials and send calendar invites to the team."

Expected Output: Structured task with title, description, priority, and due date.
```

**Social Content Testing:**

```text
Business Update: "We're launching our new delivery service in Metro Manila!"
Platform: Facebook
Tone: Excited
Target: Local customers

Expected: Filipino-friendly Facebook post with hashtags and call-to-action.
```

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
- **Setup Problems**: Check common issues section first
- **Feature Questions**: Review project roadmap in documentation
- **Team Communication**: Use project Discord/Slack channel

### Current Development Phase

🔧 **TESTING & DEBUGGING PHASE**

- Priority: Get application running locally
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

For technical questions, create an issue in this repository or contact the development team.
