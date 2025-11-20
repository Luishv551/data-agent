'use client'

import type { DataSummary } from '@/types'

interface DataSummaryProps {
  summary: DataSummary
}

export default function DataSummary({ summary }: DataSummaryProps) {
  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value)

  const formatNumber = (value: number) =>
    new Intl.NumberFormat('pt-BR').format(value)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Total Rows
        </div>
        <div className="text-2xl font-bold text-primary">
          {formatNumber(summary.total_rows)}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Total TPV
        </div>
        <div className="text-2xl font-bold text-primary">
          {formatCurrency(summary.total_tpv)}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Average Ticket
        </div>
        <div className="text-2xl font-bold text-primary">
          {formatCurrency(summary.average_ticket)}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Date Range
        </div>
        <div className="text-sm font-medium text-primary">
          {summary.date_range.start} to {summary.date_range.end}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Products
        </div>
        <div className="text-2xl font-bold text-primary">
          {summary.unique_products}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Entities
        </div>
        <div className="text-2xl font-bold text-primary">
          {summary.unique_entities}
        </div>
      </div>

      <div className="metric-card">
        <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
          Merchants
        </div>
        <div className="text-2xl font-bold text-primary">
          {formatNumber(summary.unique_merchants)}
        </div>
      </div>
    </div>
  )
}
