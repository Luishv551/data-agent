'use client'

import { useState, useEffect } from 'react'
import { getAlerts } from '@/lib/api'
import type { AlertsResponse, TopInsight } from '@/types'

interface AlertsPanelProps {
  alertsData: AlertsResponse | null
}

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value)

const formatVariation = (value: number) => {
  const sign = value >= 0 ? '+' : ''
  return `${sign}${value.toFixed(1)}%`
}

const getInsightTitle = (type: string): string => {
  switch (type) {
    case 'largest_drop': return 'Largest Drop'
    case 'main_contributor': return 'Main Contributor'
    case 'highest_growth': return 'Highest Growth'
    default: return type
  }
}

export default function AlertsPanel({ alertsData }: AlertsPanelProps) {
  // Default values: TPV for KPIs, D-30 for insights
  const [isAlertsExpanded, setIsAlertsExpanded] = useState(false)
  const [kpiMetric, setKpiMetric] = useState<'tpv' | 'average_ticket' | 'transactions'>('tpv')
  const [insightsPeriod, setInsightsPeriod] = useState<'d1' | 'd7' | 'd30'>('d30')
  const [topInsights, setTopInsights] = useState<TopInsight[]>([])
  const [dailySummary, setDailySummary] = useState(alertsData?.daily_summary)

  useEffect(() => {
    if (alertsData) {
      setTopInsights(alertsData.top_insights)
      setDailySummary(alertsData.daily_summary)
    }
  }, [alertsData])

  useEffect(() => {
    loadInsights()
  }, [insightsPeriod])

  useEffect(() => {
    loadDailySummary()
  }, [kpiMetric])

  const loadInsights = async () => {
    try {
      const data = await getAlerts(insightsPeriod, kpiMetric)
      setTopInsights(data.top_insights)
    } catch (err) {
      console.error('Failed to load insights:', err)
    }
  }

  const loadDailySummary = async () => {
    try {
      const data = await getAlerts(insightsPeriod, kpiMetric)
      setDailySummary(data.daily_summary)
    } catch (err) {
      console.error('Failed to load daily summary:', err)
    }
  }

  if (!alertsData || !dailySummary) return null

  const { alerts } = alertsData
  const increases = alerts.filter(a => a.variation > 0).length
  const decreases = alerts.filter(a => a.variation < 0).length

  const formatValue = (value: number) => {
    if (kpiMetric === 'tpv' || kpiMetric === 'average_ticket') {
      return formatCurrency(value)
    }
    return value.toLocaleString('pt-BR')
  }

  return (
    <div className="space-y-6 mb-8">
      {/* Daily Summary */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Daily KPIs</h2>
          <div className="flex gap-2">
            <button
              onClick={() => setKpiMetric('tpv')}
              className={`px-3 py-1 text-sm rounded ${
                kpiMetric === 'tpv'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              TPV
            </button>
            <button
              onClick={() => setKpiMetric('average_ticket')}
              className={`px-3 py-1 text-sm rounded ${
                kpiMetric === 'average_ticket'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              Avg Ticket
            </button>
            <button
              onClick={() => setKpiMetric('transactions')}
              className={`px-3 py-1 text-sm rounded ${
                kpiMetric === 'transactions'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              Transactions
            </button>
          </div>
        </div>

        {/* Main Metric Card */}
        <div className="card text-center mb-4">
          <p className="text-sm text-secondary mb-2">{dailySummary.date}</p>
          <p className="text-3xl font-bold mb-1">{formatValue(dailySummary.value_current)}</p>
          <p className="text-xs text-secondary">{dailySummary.metric_label}</p>
        </div>

        {/* Variation Cards */}
        <div className="grid grid-cols-3 gap-4">
          <div className="card text-center">
            <p className="text-xs text-secondary mb-2">vs D-1</p>
            <p className={`text-xl font-semibold ${dailySummary.var_d1 >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {formatVariation(dailySummary.var_d1)}
            </p>
          </div>
          <div className="card text-center">
            <p className="text-xs text-secondary mb-2">vs D-7</p>
            <p className={`text-xl font-semibold ${dailySummary.var_d7 >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {formatVariation(dailySummary.var_d7)}
            </p>
          </div>
          <div className="card text-center">
            <p className="text-xs text-secondary mb-2">vs D-30</p>
            <p className={`text-xl font-semibold ${dailySummary.var_d30 >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {formatVariation(dailySummary.var_d30)}
            </p>
          </div>
        </div>
      </div>

      {/* Top Insights */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Top Insights</h2>
          <div className="flex gap-2">
            <button
              onClick={() => setInsightsPeriod('d1')}
              className={`px-3 py-1 text-sm rounded ${
                insightsPeriod === 'd1'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              D-1
            </button>
            <button
              onClick={() => setInsightsPeriod('d7')}
              className={`px-3 py-1 text-sm rounded ${
                insightsPeriod === 'd7'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              D-7
            </button>
            <button
              onClick={() => setInsightsPeriod('d30')}
              className={`px-3 py-1 text-sm rounded ${
                insightsPeriod === 'd30'
                  ? 'bg-gray-700 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
              }`}
            >
              D-30
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {topInsights.map((insight, index) => (
            <div key={index} className="card">
              <p className="text-xs text-secondary mb-2">{getInsightTitle(insight.type)}</p>
              <p className="text-lg font-semibold mb-1">{insight.label}</p>
              <p className="text-xs text-secondary mb-2">{insight.segment_type}</p>
              <div className="flex items-center justify-between pt-2 border-t border-gray-700">
                <span className="text-xs text-secondary">TPV</span>
                <span className="text-sm">{formatCurrency(insight.value)}</span>
              </div>
              <div className="flex items-center justify-between mt-1">
                <span className="text-xs text-secondary">Change</span>
                <span className={`text-sm font-semibold ${
                  insight.variation >= 0 ? 'text-green-400' : 'text-red-400'
                }`}>
                  {formatVariation(insight.variation)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Alerts - Collapsible */}
      <div className="card">
        <button
          onClick={() => setIsAlertsExpanded(!isAlertsExpanded)}
          className="w-full flex items-center justify-between text-left"
        >
          <div>
            <h2 className="text-xl font-semibold">Anomaly Alerts</h2>
            <p className="text-xs text-secondary mt-1">14-day baseline comparison</p>
          </div>
          <div className="flex items-center gap-3">
            {alerts.length > 0 && (
              <div className="flex items-center gap-2 text-sm">
                {increases > 0 && (
                  <span className="text-green-400 font-medium">{increases}↑</span>
                )}
                {decreases > 0 && (
                  <span className="text-red-400 font-medium">{decreases}↓</span>
                )}
              </div>
            )}
            <svg
              className={`w-5 h-5 text-gray-400 transition-transform ${isAlertsExpanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>

        {isAlertsExpanded && (
          <div className="mt-4 space-y-2">
            {alerts.length > 0 ? (
              alerts.map((alert, index) => (
                <div
                  key={index}
                  className={`p-3 rounded border text-sm ${
                    alert.variation < 0
                      ? 'bg-red-950/20 border-red-800/30'
                      : 'bg-green-950/20 border-green-800/30'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="flex-1">{alert.message}</span>
                    <span className={`ml-3 font-semibold whitespace-nowrap ${
                      alert.variation < 0 ? 'text-red-400' : 'text-green-400'
                    }`}>
                      {formatVariation(alert.variation)}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-secondary text-sm py-2">No significant anomalies detected.</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
