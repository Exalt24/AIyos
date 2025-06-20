'use client'

import { Fragment } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Menu, Transition } from '@headlessui/react'
import { 
  Bars3Icon, 
  BellIcon, 
  UserCircleIcon,
  ChevronDownIcon 
} from '@heroicons/react/24/outline'
import { useAuthStore } from '@/store/auth'
import { generateAvatarUrl, getSubscriptionTierInfo, getFilipinoGreeting } from '@/lib/utils'
import { Button } from '@/components/ui/Button'

interface NavbarProps {
  onMobileMenuToggle: () => void
}

export function Navbar({ onMobileMenuToggle }: NavbarProps) {
  const { user, logout } = useAuthStore()
  const pathname = usePathname()
  
  if (!user) return null

  const avatar = generateAvatarUrl(user.company_name || user.username)
  const subscriptionInfo = getSubscriptionTierInfo(user.subscription_tier)
  const greeting = getFilipinoGreeting()

  return (
    <nav className="bg-white border-b border-gray-200 fixed top-0 right-0 left-0 lg:left-64 z-30">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Left side */}
          <div className="flex items-center">
            <button
              type="button"
              className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              onClick={onMobileMenuToggle}
              aria-label="Toggle mobile menu"
              title="Toggle mobile menu"
            >
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </button>
            
            <div className="hidden lg:flex lg:items-center lg:space-x-4">
              <h1 className="text-xl font-semibold text-gray-900">
                {greeting}
              </h1>
              <span className="text-sm text-gray-500">
                Welcome back, {user.company_name || user.username}!
              </span>
            </div>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Subscription badge */}
            <div className={`hidden sm:flex px-3 py-1 rounded-full text-xs font-medium ${subscriptionInfo.bgColor} ${subscriptionInfo.color}`}>
              {subscriptionInfo.name}
            </div>

            {/* AI usage indicator */}
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
              <span>AI Calls:</span>
              <span className="font-medium">
                {user.monthly_ai_calls} / {user.subscription_tier === 'starter' ? '1000' : user.subscription_tier === 'business' ? '5000' : '∞'}
              </span>
            </div>

            {/* Notifications */}
            <button 
              className="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              aria-label="View notifications"
              title="View notifications"
            >
              <BellIcon className="h-6 w-6" aria-hidden="true" />
            </button>

            {/* Profile dropdown */}
            <Menu as="div" className="relative">
              <Menu.Button 
                className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100"
                aria-label="User menu"
              >
                <div className={`w-8 h-8 rounded-full ${avatar.colorClass} flex items-center justify-center text-white text-sm font-medium`}>
                  {avatar.initials}
                </div>
                <ChevronDownIcon className="h-4 w-4 text-gray-400" aria-hidden="true" />
              </Menu.Button>

              <Transition
                as={Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
              >
                <Menu.Items className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <div className="py-1">
                    <Menu.Item>
                      {({ active }) => (
                        <Link
                          href="/profile"
                          className={`${active ? 'bg-gray-100' : ''} block px-4 py-2 text-sm text-gray-700`}
                        >
                          Your Profile
                        </Link>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <Link
                          href="/settings"
                          className={`${active ? 'bg-gray-100' : ''} block px-4 py-2 text-sm text-gray-700`}
                        >
                          Settings
                        </Link>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <button
                          onClick={logout}
                          className={`${active ? 'bg-gray-100' : ''} block w-full text-left px-4 py-2 text-sm text-gray-700`}
                        >
                          Sign out
                        </button>
                      )}
                    </Menu.Item>
                  </div>
                </Menu.Items>
              </Transition>
            </Menu>
          </div>
        </div>
      </div>
    </nav>
  )
}