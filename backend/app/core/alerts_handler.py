"""Alerts Handler - Calculates daily KPIs and detects anomalies."""

from datetime import timedelta
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.models.responses import DailySummary, Alert


class AlertsHandler:
    """Handles daily KPI calculations and anomaly detection."""

    def __init__(self, data_handler):
        self.data_handler = data_handler

    def get_daily_summary(self, metric: str = 'tpv') -> DailySummary:
        """Calculate daily summary with D-1, D-7, D-30 variations.

        Args:
            metric: Metric to calculate (tpv, average_ticket, transactions)
        """
        df = self.data_handler.data

        # Get the last day in dataset
        last_day = df['day'].max()
        d1 = last_day - timedelta(days=1)
        d7 = last_day - timedelta(days=7)
        d30 = last_day - timedelta(days=30)

        # Calculate metric for each period
        def calc_metric(day_data):
            if metric == 'tpv':
                return day_data['amount_transacted'].sum()
            elif metric == 'average_ticket':
                total = day_data['amount_transacted'].sum()
                count = day_data['quantity_transactions'].sum()
                return total / count if count > 0 else 0
            elif metric == 'transactions':
                return day_data['quantity_transactions'].sum()
            return 0

        value_current = calc_metric(df[df['day'] == last_day])
        value_d1 = calc_metric(df[df['day'] == d1])
        value_d7 = calc_metric(df[df['day'] == d7])
        value_d30 = calc_metric(df[df['day'] == d30])

        # Calculate variations
        var_d1 = ((value_current - value_d1) / value_d1 * 100) if value_d1 > 0 else 0
        var_d7 = ((value_current - value_d7) / value_d7 * 100) if value_d7 > 0 else 0
        var_d30 = ((value_current - value_d30) / value_d30 * 100) if value_d30 > 0 else 0

        # Metric labels
        labels = {
            'tpv': 'Total Payment Volume',
            'average_ticket': 'Average Ticket',
            'transactions': 'Total Transactions'
        }

        return DailySummary(
            date=last_day.strftime('%Y-%m-%d'),
            metric=metric,
            metric_label=labels.get(metric, 'Unknown'),
            value_current=value_current,
            var_d1=var_d1,
            var_d7=var_d7,
            var_d30=var_d30
        )

    def detect_anomalies(self) -> List[Alert]:
        """Detect anomalies in TPV and Average Ticket by segment."""
        df = self.data_handler.data
        alerts = []

        last_day = df['day'].max()
        lookback_days = 14  # Compare against 14-day average

        # Get data for last day and historical period
        current_data = df[df['day'] == last_day]
        historical_start = last_day - timedelta(days=lookback_days)
        historical_data = df[(df['day'] >= historical_start) & (df['day'] < last_day)]

        # Check TPV anomalies by product
        alerts.extend(self._check_segment_anomalies(
            current_data, historical_data, 'product', 'tpv', lookback_days
        ))

        # Check TPV anomalies by entity
        alerts.extend(self._check_segment_anomalies(
            current_data, historical_data, 'entity', 'tpv', lookback_days
        ))

        # Check Average Ticket anomalies by product
        alerts.extend(self._check_segment_anomalies(
            current_data, historical_data, 'product', 'average_ticket', lookback_days
        ))

        # Check Average Ticket anomalies by entity
        alerts.extend(self._check_segment_anomalies(
            current_data, historical_data, 'entity', 'average_ticket', lookback_days
        ))

        return alerts

    def _check_segment_anomalies(
        self,
        current_data: pd.DataFrame,
        historical_data: pd.DataFrame,
        segment: str,
        metric: str,
        lookback_days: int
    ) -> List[Alert]:
        """Check for anomalies in a specific segment and metric."""
        alerts = []

        segments = current_data[segment].unique()

        for seg_value in segments:
            current_seg = current_data[current_data[segment] == seg_value]
            historical_seg = historical_data[historical_data[segment] == seg_value]

            if len(historical_seg) == 0:
                continue

            # Calculate metric values
            if metric == 'tpv':
                current_value = current_seg['amount_transacted'].sum()
                historical_values = historical_seg.groupby('day')['amount_transacted'].sum()
            else:  # average_ticket
                current_total = current_seg['amount_transacted'].sum()
                current_count = current_seg['quantity_transactions'].sum()
                current_value = current_total / current_count if current_count > 0 else 0

                hist_grouped = historical_seg.groupby('day').agg({
                    'amount_transacted': 'sum',
                    'quantity_transactions': 'sum'
                })
                historical_values = hist_grouped['amount_transacted'] / hist_grouped['quantity_transactions']

            if len(historical_values) == 0:
                continue

            # Calculate statistics
            hist_mean = historical_values.mean()
            hist_std = historical_values.std()

            # Calculate variation percentage
            variation = ((current_value - hist_mean) / hist_mean * 100) if hist_mean > 0 else 0

            # Check if anomaly (threshold: 15% or z-score > 2)
            z_score = (current_value - hist_mean) / hist_std if hist_std > 0 else 0
            is_anomaly = abs(variation) > 15 or abs(z_score) > 2

            if is_anomaly:
                # Generate message
                metric_name = 'TPV' if metric == 'tpv' else 'Average Ticket'
                direction = 'rose' if variation > 0 else 'fell'
                message = f"{metric_name} of {seg_value} {direction} {abs(variation):.1f}%"

                alerts.append(Alert(
                    type='warning' if variation < 0 else 'info',
                    segment=segment,
                    segment_value=str(seg_value),
                    metric=metric,
                    variation=variation,
                    message=message
                ))

        return alerts

    def get_top_insights(self, period: str = 'd7') -> List:
        """Get top 3 insights for a specific period (d1, d7, d30).

        Returns:
            - Largest drop (product/entity with biggest decrease)
            - Main contributor (product/entity with highest absolute TPV)
            - Highest growth (product/entity with biggest increase)
        """
        from app.models.responses import TopInsight

        df = self.data_handler.data
        last_day = df['day'].max()

        # Determine comparison day based on period
        period_days = {'d1': 1, 'd7': 7, 'd30': 30}
        days_back = period_days.get(period, 7)
        comparison_day = last_day - timedelta(days=days_back)

        # Get data for both periods
        current_data = df[df['day'] == last_day]
        comparison_data = df[df['day'] == comparison_day]

        if len(comparison_data) == 0:
            return []

        insights = []

        # Analyze across product, entity, and payment_method
        all_variations = []

        for segment in ['product', 'entity', 'payment_method']:
            segments = current_data[segment].unique()

            for seg_value in segments:
                current_seg = current_data[current_data[segment] == seg_value]
                comparison_seg = comparison_data[comparison_data[segment] == seg_value]

                if len(comparison_seg) == 0:
                    continue

                # Calculate TPV
                current_tpv = current_seg['amount_transacted'].sum()
                comparison_tpv = comparison_seg['amount_transacted'].sum()

                if comparison_tpv > 0:
                    variation = ((current_tpv - comparison_tpv) / comparison_tpv * 100)

                    all_variations.append({
                        'segment': segment,
                        'label': str(seg_value),
                        'tpv': current_tpv,
                        'variation': variation
                    })

        if not all_variations:
            return []

        # 1. Largest drop (most negative variation)
        largest_drop = min(all_variations, key=lambda x: x['variation'])
        if largest_drop['variation'] < 0:
            insights.append(TopInsight(
                type='largest_drop',
                label=largest_drop['label'],
                segment_type=largest_drop['segment'],
                value=largest_drop['tpv'],
                variation=largest_drop['variation']
            ))

        # 2. Main contributor (highest absolute TPV)
        main_contributor = max(all_variations, key=lambda x: x['tpv'])
        insights.append(TopInsight(
            type='main_contributor',
            label=main_contributor['label'],
            segment_type=main_contributor['segment'],
            value=main_contributor['tpv'],
            variation=main_contributor['variation']
        ))

        # 3. Highest growth (most positive variation)
        highest_growth = max(all_variations, key=lambda x: x['variation'])
        if highest_growth['variation'] > 0:
            insights.append(TopInsight(
                type='highest_growth',
                label=highest_growth['label'],
                segment_type=highest_growth['segment'],
                value=highest_growth['tpv'],
                variation=highest_growth['variation']
            ))

        return insights
