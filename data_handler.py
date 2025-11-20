"""Data handler for CloudWalk transactions dataset."""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any


class DataHandler:
    """Handles loading, caching, and querying transaction data."""

    def __init__(self, csv_path: str = "transactions.csv"):
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

    def group_and_aggregate(
        self,
        group_by: List[str],
        agg_func: str = 'sum',
        filters: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """Group data and calculate aggregations.

        Args:
            group_by: List of columns to group by
            agg_func: Aggregation function ('sum', 'mean', 'count')
            filters: Optional filters to apply before grouping

        Returns:
            Aggregated dataframe
        """
        data = self.filter_data(filters) if filters else self.data.copy()

        if agg_func == 'sum':
            result = data.groupby(group_by).agg({
                'amount_transacted': 'sum',
                'quantity_transactions': 'sum',
                'quantity_of_merchants': 'sum'
            }).reset_index()
        elif agg_func == 'mean':
            result = data.groupby(group_by).agg({
                'amount_transacted': 'mean',
                'quantity_transactions': 'mean',
                'quantity_of_merchants': 'mean'
            }).reset_index()
        elif agg_func == 'count':
            result = data.groupby(group_by).size().reset_index(name='count')
        else:
            raise ValueError(f"Unsupported aggregation function: {agg_func}")

        return result

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics about the dataset.

        Returns:
            Dictionary with summary information
        """
        return {
            'total_rows': len(self.data),
            'date_range': {
                'start': self.data['day'].min().strftime('%Y-%m-%d'),
                'end': self.data['day'].max().strftime('%Y-%m-%d')
            },
            'total_tpv': self.calculate_tpv(),
            'average_ticket': self.calculate_average_ticket(),
            'unique_entities': self.data['entity'].nunique(),
            'unique_products': self.data['product'].nunique(),
            'unique_merchants': self.data['quantity_of_merchants'].sum()
        }
