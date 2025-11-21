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
    <main className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-primary mb-2">
            CloudWalk Data Agent
          </h1>
          <p className="text-secondary">
            Ask questions about your transaction data in natural language
          </p>
        </div>

        {summary && <DataSummaryComponent summary={summary} />}

        {dashboard && <DashboardCharts data={dashboard} />}

        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-primary mb-4">
            Ask Your Question
          </h2>

          <QueryInput onSubmit={handleQuery} loading={loading} />

          <ExampleQuestions onSelect={handleQuery} disabled={loading} />
        </div>

        {error && (
          <div className="card bg-red-50 border-red-200 mb-8">
            <div className="flex items-start gap-3">
              <svg
                className="w-5 h-5 text-red-500 mt-0.5"
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
                <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && <ResultsDisplay result={result} />}

        {loading && (
          <div className="card text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
            <p className="text-secondary">Processing your question...</p>
          </div>
        )}
      </div>
    </main>
  )
}
