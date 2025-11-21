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

export interface DailySummary {
  date: string
  metric: string
  metric_label: string
  value_current: number
  var_d1: number
  var_d7: number
  var_d30: number
}

export interface Alert {
  type: 'warning' | 'info'
  segment: string
  segment_value: string
  metric: string
  variation: number
  message: string
}

export interface TopInsight {
  type: 'largest_drop' | 'main_contributor' | 'highest_growth'
  label: string
  segment_type: string
  value: number
  variation: number
}

export interface AlertsResponse {
  daily_summary: DailySummary
  alerts: Alert[]
  top_insights: TopInsight[]
}
