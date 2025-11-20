'use client'

import type { QueryResponse } from '@/types'
import Chart from './Chart'

interface ResultsDisplayProps {
  result: QueryResponse
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  const formatValue = (value: any, metricType: string) => {
    if (value === null || value === undefined) return '-'

    if (metricType.includes('tpv') || metricType.includes('ticket')) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
      }).format(value)
    }

    return new Intl.NumberFormat('pt-BR').format(value)
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-primary mb-2">Results</h3>
            <p className="text-secondary">{result.explanation}</p>
          </div>
        </div>

        {result.metric_value !== null && (
          <div className="bg-surface p-4 rounded-lg mb-6">
            <div className="text-xs uppercase tracking-wide text-secondary font-semibold mb-1">
              {result.metric_name}
            </div>
            <div className="text-3xl font-bold text-primary">
              {formatValue(result.metric_value, result.query_intent.metric)}
            </div>
          </div>
        )}

        {result.data.length > 0 && (
          <>
            <div className="overflow-x-auto mb-6">
              <table className="table">
                <thead>
                  <tr>
                    {Object.keys(result.data[0]).map((key) => (
                      <th key={key}>{key.replace(/_/g, ' ')}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.data.map((row, index) => (
                    <tr key={index}>
                      {Object.entries(row).map(([key, value]) => (
                        <td key={key}>
                          {key === 'metric_value'
                            ? formatValue(value, result.query_intent.metric)
                            : String(value)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {result.data.length > 1 && result.data[0].metric_value !== undefined && (
              <Chart data={result.data} queryIntent={result.query_intent} />
            )}
          </>
        )}
      </div>

      <details className="card">
        <summary className="cursor-pointer text-sm font-semibold text-secondary uppercase tracking-wide">
          Query Details
        </summary>
        <pre className="mt-4 p-4 bg-surface rounded text-xs overflow-x-auto">
          {JSON.stringify(result.query_intent, null, 2)}
        </pre>
      </details>
    </div>
  )
}
