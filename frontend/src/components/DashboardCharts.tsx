'use client'

import { useState } from 'react'
import type { DashboardData } from '@/types'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface DashboardChartsProps {
  data: DashboardData
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

type TPVGrouping = 'product' | 'entity' | 'payment_method'
type InsightGrouping = 'price_tier' | 'installments'

export default function DashboardCharts({ data }: DashboardChartsProps) {
  const [tpvGrouping, setTpvGrouping] = useState<TPVGrouping>('product')
  const [ticketGrouping, setTicketGrouping] = useState<TPVGrouping>('entity')
  const [insightGrouping, setInsightGrouping] = useState<InsightGrouping>('price_tier')

  const getTPVData = (grouping: TPVGrouping) => {
    switch (grouping) {
      case 'product':
        return { data: data.tpv_by_product, key: 'product' }
      case 'entity':
        return { data: data.tpv_by_entity, key: 'entity' }
      case 'payment_method':
        return { data: data.tpv_by_payment_method, key: 'payment_method' }
    }
  }

  const getTicketData = (grouping: TPVGrouping) => {
    switch (grouping) {
      case 'product':
        return { data: data.avg_ticket_by_product, key: 'product' }
      case 'entity':
        return { data: data.avg_ticket_by_entity, key: 'entity' }
      case 'payment_method':
        return { data: data.avg_ticket_by_payment_method, key: 'payment_method' }
    }
  }

  const getInsightData = (grouping: InsightGrouping) => {
    switch (grouping) {
      case 'price_tier':
        return { data: data.tpv_by_price_tier, key: 'price_tier' }
      case 'installments':
        return { data: data.tpv_by_installments, key: 'installments' }
    }
  }

  const tpvChart = getTPVData(tpvGrouping)
  const ticketChart = getTicketData(ticketGrouping)
  const insightChart = getInsightData(insightGrouping)

  const tooltipStyle = {
    backgroundColor: '#1f2937',
    border: '1px solid #374151',
    borderRadius: '8px',
    fontSize: '14px',
    color: '#f3f4f6'
  }

  const cursorStyle = { fill: '#374151' }

  return (
    <div className="space-y-6 mb-8">
      <h2 className="text-xl font-semibold text-white">Business Insights</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
              TPV Analysis
            </h3>
            <select
              value={tpvGrouping}
              onChange={(e) => setTpvGrouping(e.target.value as TPVGrouping)}
              className="text-sm border border-gray-600 rounded px-2 py-1 bg-gray-800 text-gray-200"
            >
              <option value="product">by Product</option>
              <option value="entity">by Entity</option>
              <option value="payment_method">by Payment Method</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tpvChart.data} layout="vertical">
                <defs>
                  <linearGradient id="tpvGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#4b5563" />
                    <stop offset="100%" stopColor="#6b7280" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" tickFormatter={formatCurrency} tick={{ fontSize: 11, fill: '#9ca3af' }} stroke="#4b5563" />
                <YAxis dataKey={tpvChart.key} type="category" tick={{ fontSize: 12, fill: '#9ca3af' }} width={100} stroke="#4b5563" />
                <Tooltip formatter={(value: number) => formatTooltipValue(value)} contentStyle={tooltipStyle} cursor={cursorStyle} />
                <Bar dataKey="amount_transacted" fill="url(#tpvGradient)" name="TPV" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
              Average Ticket
            </h3>
            <select
              value={ticketGrouping}
              onChange={(e) => setTicketGrouping(e.target.value as TPVGrouping)}
              className="text-sm border border-gray-600 rounded px-2 py-1 bg-gray-800 text-gray-200"
            >
              <option value="product">by Product</option>
              <option value="entity">by Entity</option>
              <option value="payment_method">by Payment Method</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ticketChart.data} layout="vertical">
                <defs>
                  <linearGradient id="ticketGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#4b5563" />
                    <stop offset="100%" stopColor="#6b7280" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" tickFormatter={formatCurrency} tick={{ fontSize: 11, fill: '#9ca3af' }} stroke="#4b5563" />
                <YAxis dataKey={ticketChart.key} type="category" tick={{ fontSize: 12, fill: '#9ca3af' }} width={100} stroke="#4b5563" />
                <Tooltip formatter={(value: number) => formatTooltipValue(value)} contentStyle={tooltipStyle} cursor={cursorStyle} />
                <Bar dataKey="average_ticket" fill="url(#ticketGradient)" name="Avg Ticket" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
              Transactional Insights
            </h3>
            <select
              value={insightGrouping}
              onChange={(e) => setInsightGrouping(e.target.value as InsightGrouping)}
              className="text-sm border border-gray-600 rounded px-2 py-1 bg-gray-800 text-gray-200"
            >
              <option value="price_tier">by Price Tier</option>
              <option value="installments">by Installments</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={insightChart.data}>
                <defs>
                  <linearGradient id="insightGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6b7280" />
                    <stop offset="100%" stopColor="#4b5563" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey={insightChart.key} tick={{ fontSize: 12, fill: '#9ca3af' }} stroke="#4b5563" />
                <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 11, fill: '#9ca3af' }} stroke="#4b5563" width={80} />
                <Tooltip formatter={(value: number) => formatTooltipValue(value)} contentStyle={tooltipStyle} cursor={cursorStyle} />
                <Bar dataKey="amount_transacted" fill="url(#insightGradient)" name="TPV" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}
