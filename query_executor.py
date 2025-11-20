"""Query executor that bridges LLM intents and data operations."""

import pandas as pd
from typing import Dict, Any, Optional
from data_handler import DataHandler


class QueryResult:
    """Container for query execution results."""

    def __init__(
        self,
        data: pd.DataFrame,
        metric_value: Optional[float],
        metric_name: str,
        explanation: str,
        query_intent: Dict[str, Any]
    ):
        """Initialize query result.

        Args:
            data: Result dataframe
            metric_value: Single metric value if applicable
            metric_name: Name of the calculated metric
            explanation: Explanation of what was computed
            query_intent: Original query intent from LLM
        """
        self.data = data
        self.metric_value = metric_value
        self.metric_name = metric_name
        self.explanation = explanation
        self.query_intent = query_intent

    def __repr__(self) -> str:
        return f"QueryResult(metric={self.metric_name}, value={self.metric_value}, rows={len(self.data)})"


class QueryExecutor:
    """Executes queries based on LLM-generated intents."""

    def __init__(self, data_handler: DataHandler):
        """Initialize the query executor.

        Args:
            data_handler: DataHandler instance for data operations
        """
        self.data_handler = data_handler

    def execute(self, query_intent: Dict[str, Any]) -> QueryResult:
        """Execute a query based on LLM intent.

        Args:
            query_intent: Structured query intent from LLM

        Returns:
            QueryResult with computed data and metrics
        """
        metric = query_intent['metric']
        aggregation = query_intent['aggregation']
        group_by = query_intent['group_by']
        filters = query_intent.get('filters', {})
        sort_by = query_intent.get('sort_by', 'metric')
        sort_order = query_intent.get('sort_order', 'desc')
        limit = query_intent.get('limit')
        explanation = query_intent.get('explanation', 'Query executed')

        filtered_data = self.data_handler.filter_data(filters) if filters else self.data_handler.data

        if group_by:
            result_df = self._execute_grouped_query(
                filtered_data, metric, aggregation, group_by
            )
        else:
            result_df = self._execute_simple_query(filtered_data, metric)

        if sort_by == 'metric' and 'metric_value' in result_df.columns:
            result_df = result_df.sort_values(
                'metric_value',
                ascending=(sort_order == 'asc')
            )

        if limit and isinstance(limit, int):
            result_df = result_df.head(limit)

        metric_value = None
        if len(result_df) == 1 and 'metric_value' in result_df.columns:
            metric_value = float(result_df.iloc[0]['metric_value'])

        metric_name = self._get_metric_name(metric)

        return QueryResult(
            data=result_df,
            metric_value=metric_value,
            metric_name=metric_name,
            explanation=explanation,
            query_intent=query_intent
        )

    def _execute_grouped_query(
        self,
        data: pd.DataFrame,
        metric: str,
        aggregation: str,
        group_by: list
    ) -> pd.DataFrame:
        """Execute a grouped query with aggregation.

        Args:
            data: Filtered dataset
            metric: Metric to calculate
            aggregation: Aggregation function
            group_by: Columns to group by

        Returns:
            Aggregated dataframe
        """
        if metric == 'tpv':
            grouped = data.groupby(group_by).agg({
                'amount_transacted': 'sum'
            }).reset_index()
            grouped['metric_value'] = grouped['amount_transacted']

        elif metric == 'average_ticket':
            grouped = data.groupby(group_by).agg({
                'amount_transacted': 'sum',
                'quantity_transactions': 'sum'
            }).reset_index()
            grouped['metric_value'] = (
                grouped['amount_transacted'] / grouped['quantity_transactions']
            )

        elif metric == 'transactions':
            grouped = data.groupby(group_by).agg({
                'quantity_transactions': 'sum'
            }).reset_index()
            grouped['metric_value'] = grouped['quantity_transactions']

        elif metric == 'merchants':
            grouped = data.groupby(group_by).agg({
                'quantity_of_merchants': 'sum'
            }).reset_index()
            grouped['metric_value'] = grouped['quantity_of_merchants']

        else:
            raise ValueError(f"Unsupported metric: {metric}")

        return grouped

    def _execute_simple_query(self, data: pd.DataFrame, metric: str) -> pd.DataFrame:
        """Execute a simple query without grouping.

        Args:
            data: Filtered dataset
            metric: Metric to calculate

        Returns:
            DataFrame with single metric value
        """
        if metric == 'tpv':
            value = self.data_handler.calculate_tpv(data)
        elif metric == 'average_ticket':
            value = self.data_handler.calculate_average_ticket(data)
        elif metric == 'transactions':
            value = data['quantity_transactions'].sum()
        elif metric == 'merchants':
            value = data['quantity_of_merchants'].sum()
        else:
            raise ValueError(f"Unsupported metric: {metric}")

        return pd.DataFrame([{'metric_value': value}])

    def _get_metric_name(self, metric: str) -> str:
        """Get human-readable metric name.

        Args:
            metric: Metric identifier

        Returns:
            Human-readable name
        """
        metric_names = {
            'tpv': 'Total Payment Volume (TPV)',
            'average_ticket': 'Average Ticket',
            'transactions': 'Total Transactions',
            'merchants': 'Total Merchants'
        }
        return metric_names.get(metric, metric)
