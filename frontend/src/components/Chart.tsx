'use client'

import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import type { QueryIntent } from '@/types'

interface ChartProps {
  data: Array<Record<string, any>>
  queryIntent: QueryIntent
}

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value)

const formatTooltipValue = (value: number) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value)

const formatNumber = (value: number) =>
  new Intl.NumberFormat('pt-BR', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value)

export default function Chart({ data, queryIntent }: ChartProps) {
  const groupBy = queryIntent.group_by[0]
  const isTimeSeries = groupBy === 'day'
  const isDayOfWeek = groupBy === 'day_of_week'
  const isCurrency = queryIntent.metric === 'tpv' || queryIntent.metric === 'average_ticket'

  const chartData = data.map(row => ({
    name: String(row[groupBy]),
    value: Number(row.metric_value)
  }))

  const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const sortedData = isDayOfWeek
    ? chartData.sort((a, b) => dayOrder.indexOf(a.name) - dayOrder.indexOf(b.name))
    : chartData

  const yAxisFormatter = (value: number) => {
    if (isCurrency) return formatCurrency(value)
    return formatNumber(value)
  }

  const commonChartElements = (
    <>
      <defs>
        <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#374151" />
          <stop offset="100%" stopColor="#1f2937" />
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
      <XAxis
        dataKey="name"
        stroke="#9ca3af"
        style={{ fontSize: '12px' }}
        tick={{ fill: '#9ca3af' }}
      />
      <YAxis
        stroke="#9ca3af"
        style={{ fontSize: '11px' }}
        tick={{ fill: '#9ca3af' }}
        width={90}
        tickFormatter={yAxisFormatter}
      />
      <Tooltip
        contentStyle={{
          backgroundColor: '#1f2937',
          border: '1px solid #374151',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#f3f4f6'
        }}
        cursor={{ fill: '#374151' }}
        formatter={(value: number) => [isCurrency ? formatTooltipValue(value) : value.toLocaleString('pt-BR'), 'Value']}
      />
    </>
  )

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        {isTimeSeries ? (
          <LineChart data={sortedData}>
            {commonChartElements}
            <Line
              dataKey="value"
              stroke="url(#barGradient)"
              strokeWidth={2}
            />
          </LineChart>
        ) : (
          <BarChart data={sortedData}>
            {commonChartElements}
            <Bar
              dataKey="value"
              fill="url(#barGradient)"
            />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  )
}
