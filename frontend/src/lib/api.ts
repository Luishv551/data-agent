import axios from 'axios'
import type { DataSummary, DashboardData, QueryRequest, QueryResponse, AlertsResponse } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getDataSummary = async (): Promise<DataSummary> => {
  const { data } = await api.get<DataSummary>('/data/summary')
  return data
}

export const getDashboardData = async (): Promise<DashboardData> => {
  const { data } = await api.get<DashboardData>('/data/dashboard')
  return data
}

export const processQuery = async (request: QueryRequest): Promise<QueryResponse> => {
  const { data } = await api.post<QueryResponse>('/query', request)
  return data
}

export const checkHealth = async (): Promise<{ status: string; version: string }> => {
  const { data } = await api.get('/')
  return data
}

export const getAlerts = async (
  period: 'd1' | 'd7' | 'd30' = 'd30',
  metric: 'tpv' | 'average_ticket' | 'transactions' = 'tpv'
): Promise<AlertsResponse> => {
  const { data } = await api.get<AlertsResponse>('/alerts', {
    params: { period, metric }
  })
  return data
}
