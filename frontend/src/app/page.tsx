'use client'

import { useState, useEffect } from 'react'
import { getDataSummary, getDashboardData, processQuery } from '@/lib/api'
import type { DataSummary, DashboardData, QueryResponse } from '@/types'
import DataSummaryComponent from '@/components/DataSummary'
import DashboardCharts from '@/components/DashboardCharts'
import QueryInput from '@/components/QueryInput'
import ExampleQuestions from '@/components/ExampleQuestions'
import ResultsDisplay from '@/components/ResultsDisplay'

export default function Home() {
  const [summary, setSummary] = useState<DataSummary | null>(null)
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<QueryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [summaryData, dashboardData] = await Promise.all([
        getDataSummary(),
        getDashboardData()
      ])
      setSummary(summaryData)
      setDashboard(dashboardData)
    } catch (err) {
      console.error('Failed to load data:', err)
    }
  }

  const handleQuery = async (question: string) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await processQuery({ question })
      setResult(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process query. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-dark">
      <header className="relative overflow-hidden mb-8">
        <div className="absolute inset-0 bg-gradient-to-r from-dark-300 via-dark-200 to-dark opacity-90" />
        <div className="relative max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center gap-6">
            <img
              src="/logo.png"
              alt="CloudWalk"
              className="h-10 w-auto brightness-0 invert"
            />
            <div>
              <h1 className="text-2xl font-bold text-white">
                Data Agent
              </h1>
              <p className="text-gray-400 text-sm">
                Natural language analytics for transaction data
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 pb-12 sm:px-6 lg:px-8">
        {summary && <DataSummaryComponent summary={summary} />}

        {dashboard && <DashboardCharts data={dashboard} />}

        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">
            Ask Your Question
          </h2>

          <QueryInput onSubmit={handleQuery} loading={loading} />

          <ExampleQuestions onSelect={handleQuery} disabled={loading} />
        </div>

        {error && (
          <div className="card bg-red-900/20 border-red-800 mb-8">
            <div className="flex items-start gap-3">
              <svg
                className="w-5 h-5 text-red-400 mt-0.5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="font-semibold text-red-300 mb-1">Error</h3>
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && <ResultsDisplay result={result} />}

        {loading && (
          <div className="card text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-accent mb-4"></div>
            <p className="text-gray-400">Processing your question...</p>
          </div>
        )}
      </div>
    </main>
  )
}
