export interface DataSummary {
  total_tpv: number
  average_ticket: number
}

export interface DashboardData {
  tpv_by_product: Array<{ product: string; amount_transacted: number }>
  tpv_by_entity: Array<{ entity: string; amount_transacted: number }>
  tpv_by_payment_method: Array<{ payment_method: string; amount_transacted: number }>
  avg_ticket_by_entity: Array<{ entity: string; average_ticket: number }>
  avg_ticket_by_product: Array<{ product: string; average_ticket: number }>
  avg_ticket_by_payment_method: Array<{ payment_method: string; average_ticket: number }>
  tpv_by_price_tier: Array<{ price_tier: string; amount_transacted: number }>
  tpv_by_installments: Array<{ installments: number; amount_transacted: number }>
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
