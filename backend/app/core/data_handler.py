"""Data handler for CloudWalk transactions dataset."""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any


class DataHandler:
    """Handles loading, caching, and querying transaction data."""

    def __init__(self, csv_path: str | Path):
        """Initialize the data handler.

        Args:
            csv_path: Path to the transactions CSV file
        """
        self.csv_path = Path(csv_path)
        self._data: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self) -> None:
        """Load CSV data into memory and perform initial processing."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self._data = pd.read_csv(self.csv_path)
        self._data['day'] = pd.to_datetime(self._data['day'])
        self._data['day_of_week'] = self._data['day'].dt.day_name()

    @property
    def data(self) -> pd.DataFrame:
        """Get the loaded dataset."""
        if self._data is None:
            raise RuntimeError("Data not loaded")
        return self._data

    def get_column_names(self) -> List[str]:
        """Get list of all column names."""
        return list(self.data.columns)

    def get_unique_values(self, column: str) -> List[Any]:
        """Get unique values for a specific column.

        Args:
            column: Column name

        Returns:
            List of unique values
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        return self.data[column].unique().tolist()

    def calculate_tpv(self, df: Optional[pd.DataFrame] = None) -> float:
        """Calculate Total Payment Volume (sum of amount_transacted).

        Args:
            df: Optional dataframe subset. If None, uses full dataset.

        Returns:
            Total payment volume
        """
        data = df if df is not None else self.data
        return float(data['amount_transacted'].sum())

    def calculate_average_ticket(self, df: Optional[pd.DataFrame] = None) -> float:
        """Calculate Average Ticket (amount_transacted / quantity_transactions).

        Args:
            df: Optional dataframe subset. If None, uses full dataset.

        Returns:
            Average ticket value
        """
        data = df if df is not None else self.data
        total_amount = data['amount_transacted'].sum()
        total_transactions = data['quantity_transactions'].sum()

        if total_transactions == 0:
            return 0.0

        return float(total_amount / total_transactions)

    def filter_data(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on column values.

        Args:
            filters: Dictionary of column_name: value pairs

        Returns:
            Filtered dataframe
        """
        filtered = self.data.copy()

        for column, value in filters.items():
            if column not in filtered.columns:
                raise ValueError(f"Column '{column}' not found")

            if isinstance(value, list):
                filtered = filtered[filtered[column].isin(value)]
            else:
                filtered = filtered[filtered[column] == value]

        return filtered

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics about the dataset.

        Returns:
            Dictionary with summary information
        """
        return {
            'total_tpv': self.calculate_tpv(),
            'average_ticket': self.calculate_average_ticket()
        }

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get pre-aggregated data for dashboard visualizations.

        Returns:
            Dictionary with dashboard chart data
        """
        # TPV by product
        tpv_by_product = self.data.groupby('product').agg({
            'amount_transacted': 'sum'
        }).reset_index()
        tpv_by_product = tpv_by_product.sort_values('amount_transacted', ascending=False)

        # TPV by entity
        tpv_by_entity = self.data.groupby('entity').agg({
            'amount_transacted': 'sum'
        }).reset_index()

        # TPV by payment_method
        tpv_by_payment = self.data.groupby('payment_method').agg({
            'amount_transacted': 'sum'
        }).reset_index()
        tpv_by_payment = tpv_by_payment.sort_values('amount_transacted', ascending=False)

        # Average ticket by entity
        avg_ticket_by_entity = self.data.groupby('entity').agg({
            'amount_transacted': 'sum',
            'quantity_transactions': 'sum'
        }).reset_index()
        avg_ticket_by_entity['average_ticket'] = (
            avg_ticket_by_entity['amount_transacted'] / avg_ticket_by_entity['quantity_transactions']
        )
        avg_ticket_by_entity = avg_ticket_by_entity[['entity', 'average_ticket']]

        # Average ticket by product
        avg_ticket_by_product = self.data.groupby('product').agg({
            'amount_transacted': 'sum',
            'quantity_transactions': 'sum'
        }).reset_index()
        avg_ticket_by_product['average_ticket'] = (
            avg_ticket_by_product['amount_transacted'] / avg_ticket_by_product['quantity_transactions']
        )
        avg_ticket_by_product = avg_ticket_by_product[['product', 'average_ticket']]
        avg_ticket_by_product = avg_ticket_by_product.sort_values('average_ticket', ascending=False)

        # Average ticket by payment_method
        avg_ticket_by_payment = self.data.groupby('payment_method').agg({
            'amount_transacted': 'sum',
            'quantity_transactions': 'sum'
        }).reset_index()
        avg_ticket_by_payment['average_ticket'] = (
            avg_ticket_by_payment['amount_transacted'] / avg_ticket_by_payment['quantity_transactions']
        )
        avg_ticket_by_payment = avg_ticket_by_payment[['payment_method', 'average_ticket']]
        avg_ticket_by_payment = avg_ticket_by_payment.sort_values('average_ticket', ascending=False)

        # TPV by price_tier
        tpv_by_price_tier = self.data.groupby('price_tier').agg({
            'amount_transacted': 'sum'
        }).reset_index()
        tpv_by_price_tier = tpv_by_price_tier.sort_values('amount_transacted', ascending=False)

        # TPV by installments
        tpv_by_installments = self.data.groupby('installments').agg({
            'amount_transacted': 'sum'
        }).reset_index()
        tpv_by_installments = tpv_by_installments.sort_values('installments')

        return {
            'tpv_by_product': tpv_by_product.to_dict(orient='records'),
            'tpv_by_entity': tpv_by_entity.to_dict(orient='records'),
            'tpv_by_payment_method': tpv_by_payment.to_dict(orient='records'),
            'avg_ticket_by_entity': avg_ticket_by_entity.to_dict(orient='records'),
            'avg_ticket_by_product': avg_ticket_by_product.to_dict(orient='records'),
            'avg_ticket_by_payment_method': avg_ticket_by_payment.to_dict(orient='records'),
            'tpv_by_price_tier': tpv_by_price_tier.to_dict(orient='records'),
            'tpv_by_installments': tpv_by_installments.to_dict(orient='records')
        }
