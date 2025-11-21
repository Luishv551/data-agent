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

  return (
    <div className="space-y-6 mb-8">
      <h2 className="text-xl font-semibold text-primary">Business Insights</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-secondary uppercase tracking-wide">
              TPV Analysis
            </h3>
            <select
              value={tpvGrouping}
              onChange={(e) => setTpvGrouping(e.target.value as TPVGrouping)}
              className="text-sm border border-surface-dark rounded px-2 py-1 bg-white"
            >
              <option value="product">by Product</option>
              <option value="entity">by Entity</option>
              <option value="payment_method">by Payment Method</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tpvChart.data} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E0" />
                <XAxis type="number" tickFormatter={formatCurrency} tick={{ fontSize: 11 }} />
                <YAxis dataKey={tpvChart.key} type="category" tick={{ fontSize: 12 }} width={100} />
                <Tooltip formatter={(value: number) => formatCurrency(value)} />
                <Bar dataKey="amount_transacted" fill="#1A1A1A" name="TPV" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-secondary uppercase tracking-wide">
              Average Ticket
            </h3>
            <select
              value={ticketGrouping}
              onChange={(e) => setTicketGrouping(e.target.value as TPVGrouping)}
              className="text-sm border border-surface-dark rounded px-2 py-1 bg-white"
            >
              <option value="product">by Product</option>
              <option value="entity">by Entity</option>
              <option value="payment_method">by Payment Method</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ticketChart.data} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E0" />
                <XAxis type="number" tickFormatter={formatCurrency} tick={{ fontSize: 11 }} />
                <YAxis dataKey={ticketChart.key} type="category" tick={{ fontSize: 12 }} width={100} />
                <Tooltip formatter={(value: number) => formatCurrency(value)} />
                <Bar dataKey="average_ticket" fill="#666666" name="Avg Ticket" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-secondary uppercase tracking-wide">
              Transactional Insights
            </h3>
            <select
              value={insightGrouping}
              onChange={(e) => setInsightGrouping(e.target.value as InsightGrouping)}
              className="text-sm border border-surface-dark rounded px-2 py-1 bg-white"
            >
              <option value="price_tier">by Price Tier</option>
              <option value="installments">by Installments</option>
            </select>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={insightChart.data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E0" />
                <XAxis dataKey={insightChart.key} tick={{ fontSize: 12 }} />
                <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(value: number) => formatCurrency(value)} />
                <Bar dataKey="amount_transacted" fill="#1A1A1A" name="TPV" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}
