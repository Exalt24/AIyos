import { existsSync, readFileSync } from 'fs';
import path from 'path';

const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

const log = (message, color = 'reset') => {
  console.log(`${colors[color]}${message}${colors.reset}`);
};

const checkFile = (filePath, description) => {
  if (existsSync(filePath)) {
    log(`✅ ${description}`, 'green');
    return true;
  } else {
    log(`❌ ${description}`, 'red');
    return false;
  }
};

const checkEnvVariable = (envPath, variable, description) => {
  if (!existsSync(envPath)) return false;
  
  const envContent = readFileSync(envPath, 'utf8');
  
  // Check if variable exists and has a non-placeholder value
  const variablePattern = new RegExp(`^${variable}=(.+)$`, 'm');
  const match = envContent.match(variablePattern);
  
  if (match && match[1]) {
    const value = match[1].trim();
    // Check if it's not a placeholder value
    const isPlaceholder = value.includes('your_') || 
                         value.includes('your-') || 
                         value.includes('change-in-production') ||
                         value === '' ||
                         value.includes('api_key_here') ||
                         value.includes('secret-key-here');
    
    if (!isPlaceholder) {
      log(`✅ ${description}`, 'green');
      return true;
    } else {
      log(`❌ ${description} (placeholder value found)`, 'red');
      return false;
    }
  } else {
    log(`❌ ${description} (missing or empty)`, 'red');
    return false;
  }
};

console.log('\n' + '='.repeat(60));
log('🚀 AIyos Development Environment Check', 'bold');
console.log('='.repeat(60));

let allGood = true;

// Check project structure
log('\n📁 Project Structure:', 'blue');
allGood &= checkFile('backend', 'Backend directory exists');
allGood &= checkFile('frontend', 'Frontend directory exists');
allGood &= checkFile('backend/manage.py', 'Django manage.py exists');
allGood &= checkFile('frontend/package.json', 'Frontend package.json exists');

// Check backend setup
log('\n🐍 Backend (Django) Setup:', 'blue');
allGood &= checkFile('backend/venv', 'Python virtual environment exists');
allGood &= checkFile('backend/requirements.txt', 'Requirements.txt exists');
allGood &= checkFile('backend/.env', 'Backend .env file exists');

if (existsSync('backend/.env')) {
  log('\n🔐 Backend Environment Variables:', 'yellow');
  checkEnvVariable('backend/.env', 'SECRET_KEY', 'Django SECRET_KEY configured');
  checkEnvVariable('backend/.env', 'OPENROUTER_API_KEY', 'OpenRouter API key configured');
  checkEnvVariable('backend/.env', 'DATABASE_URL', 'Database URL configured');
}

// Check frontend setup
log('\n⚛️  Frontend (Next.js) Setup:', 'blue');
allGood &= checkFile('frontend/node_modules', 'Frontend dependencies installed');
allGood &= checkFile('frontend/.env.local', 'Frontend .env.local file exists');
allGood &= checkFile('frontend/src', 'Frontend src directory exists');

if (existsSync('frontend/.env.local')) {
  log('\n🔐 Frontend Environment Variables:', 'yellow');
  checkEnvVariable('frontend/.env.local', 'NEXT_PUBLIC_API_URL', 'API URL configured');
  checkEnvVariable('frontend/.env.local', 'NEXT_PUBLIC_APP_NAME', 'App name configured');
}

// Check database
log('\n🗄️  Database:', 'blue');
const dbExists = checkFile('backend/db.sqlite3', 'SQLite database exists (run migrations if missing)');

// Summary
console.log('\n' + '='.repeat(60));
if (allGood && dbExists) {
  log('✅ Environment looks good! You can run: npm run dev', 'green');
} else {
  log('❌ Some issues found. Please check the items above.', 'red');
  
  console.log('\n📋 Quick Setup Commands:');
  log('1. Initial setup: npm run setup', 'yellow');
  log('2. Install dependencies only: npm run setup:quick', 'yellow');
  log('3. Create database: npm run backend:migrate', 'yellow');
  log('4. Create admin user: npm run backend:superuser', 'yellow');
  log('5. Start development: npm run dev', 'yellow');
}

console.log('\n📚 Useful Commands:');
log('• npm run dev          - Start both servers', 'blue');
log('• npm run backend:dev  - Start Django only', 'blue');
log('• npm run frontend:dev - Start Next.js only', 'blue');
log('• npm run check:env    - Run this check again', 'blue');
log('• npm run clean        - Clean cache files', 'blue');

console.log('\n🌐 URLs:');
log('• Frontend: http://localhost:3000', 'blue');
log('• Backend API: http://localhost:8000/api', 'blue');
log('• Django Admin: http://localhost:8000/admin', 'blue');
log('• API Docs: http://localhost:8000/api/docs', 'blue');

console.log('='.repeat(60) + '\n');