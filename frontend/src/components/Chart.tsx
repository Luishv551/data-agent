'use client'

import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import type { QueryIntent } from '@/types'

interface ChartProps {
  data: Array<Record<string, any>>
  queryIntent: QueryIntent
}

export default function Chart({ data, queryIntent }: ChartProps) {
  const groupBy = queryIntent.group_by[0]
  const isTimeSeries = groupBy === 'day'
  const isDayOfWeek = groupBy === 'day_of_week'

  const chartData = data.map(row => ({
    name: String(row[groupBy]),
    value: Number(row.metric_value)
  }))

  const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const sortedData = isDayOfWeek
    ? chartData.sort((a, b) => dayOrder.indexOf(a.name) - dayOrder.indexOf(b.name))
    : chartData

  const ChartComponent = isTimeSeries ? LineChart : BarChart
  const DataComponent = isTimeSeries ? Line : Bar

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <ChartComponent data={sortedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E0" />
          <XAxis
            dataKey="name"
            stroke="#666666"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            stroke="#666666"
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E0E0E0',
              borderRadius: '8px',
              fontSize: '14px'
            }}
          />
          <DataComponent
            dataKey="value"
            fill="#1A1A1A"
            stroke="#1A1A1A"
            strokeWidth={isTimeSeries ? 2 : 0}
          />
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  )
}
