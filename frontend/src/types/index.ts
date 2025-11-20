export interface DataSummary {
  total_rows: number
  date_range: {
    start: string
    end: string
  }
  total_tpv: number
  average_ticket: number
  unique_entities: number
  unique_products: number
  unique_merchants: number
}

export interface QueryIntent {
  metric: 'tpv' | 'average_ticket' | 'transactions' | 'merchants'
  aggregation: 'sum' | 'mean' | 'count'
  group_by: string[]
  filters: Record<string, any>
  sort_by?: string
  sort_order?: 'desc' | 'asc'
  limit?: number | null
  explanation: string
}

export interface QueryResponse {
  data: Array<Record<string, any>>
  metric_value: number | null
  metric_name: string
  explanation: string
  query_intent: QueryIntent
}

export interface QueryRequest {
  question: string
}
