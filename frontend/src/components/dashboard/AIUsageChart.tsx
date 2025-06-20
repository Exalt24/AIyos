'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'

interface AIUsageChartProps {
  data: Array<{
    date: string
    requests: number
    cost: number
  }>
}

export function AIUsageChart({ data }: AIUsageChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Usage This Week</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'requests' ? `${value} requests` : `₱${value}`,
                  name === 'requests' ? 'AI Requests' : 'Cost (PHP)'
                ]}
              />
              <Bar dataKey="requests" fill="#3b82f6" name="requests" />
              <Bar dataKey="cost" fill="#10b981" name="cost" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}