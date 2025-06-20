import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AIyos - AI Automation para sa Filipino SMBs',
  description: 'AI-powered workflow automation that gets Filipino businesses organized. Simpler than Zapier, more affordable than enterprise tools.',
  keywords: 'AI automation, Filipino business, workflow automation, Philippines, SMB, BPO, artificial intelligence',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#333',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            },
          }}
        />
      </body>
    </html>
  )
}