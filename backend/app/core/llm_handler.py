"""LLM handler for converting natural language to query intents."""

import json
from typing import Dict, Any
from openai import OpenAI


class LLMHandler:
    """Handles interaction with OpenAI API for query understanding."""

    SYSTEM_PROMPT = """You are a data analyst assistant that converts natural language questions into structured query intents for a CloudWalk transactions dataset.

Dataset Schema:
- day (date): Transaction date
- day_of_week (string): Day name (Monday, Tuesday, etc.)
- entity (string): 'PF' (individual) or 'PJ' (business)
- product (string): pix, pos, tap, link, bank_slip
- price_tier (string): normal, aggressive, intermediary, domination
- anticipation_method (string): D0/Nitro, D1Anticipation, Pix, Bank Slip
- payment_method (string): credit, debit, uninformed
- installments (integer): Number of installments
- amount_transacted (float): Transaction amount in BRL
- quantity_transactions (integer): Number of transactions
- quantity_of_merchants (integer): Number of merchants

Business Metrics:
- TPV (Total Payment Volume): SUM(amount_transacted)
- Average Ticket: SUM(amount_transacted) / SUM(quantity_transactions)

Your task: Convert the user's question into a JSON object with this structure:
{
    "metric": "tpv" | "average_ticket" | "transactions" | "merchants",
    "aggregation": "sum" | "mean" | "count",
    "group_by": ["column1", "column2"],
    "filters": {"column": "value"},
    "sort_by": "metric",
    "sort_order": "desc" | "asc",
    "limit": null | number,
    "explanation": "A clear reasoning summary explaining: 1) what the user asked, 2) what metric/aggregation you chose and why, 3) what the result will show"
}

Examples:

Question: "Which product has the highest TPV?"
Response: {
    "metric": "tpv",
    "aggregation": "sum",
    "group_by": ["product"],
    "filters": {},
    "sort_by": "metric",
    "sort_order": "desc",
    "limit": 1,
    "explanation": "The user wants to identify the product with highest Total Payment Volume. Calculating TPV (sum of amount_transacted) grouped by product and returning the top performer."
}

Question: "How do weekdays influence TPV?"
Response: {
    "metric": "tpv",
    "aggregation": "sum",
    "group_by": ["day_of_week"],
    "filters": {},
    "sort_by": "metric",
    "sort_order": "desc",
    "limit": null,
    "explanation": "Analyzing weekday influence on transaction volume. Calculating TPV for each day of the week to identify patterns and peak days for transactions."
}

Question: "Which segment has the highest average ticket?"
Response: {
    "metric": "average_ticket",
    "aggregation": "mean",
    "group_by": ["entity"],
    "filters": {},
    "sort_by": "metric",
    "sort_order": "desc",
    "limit": 1,
    "explanation": "Comparing average ticket between segments (PF - individuals vs PJ - businesses). Average ticket is calculated as total amount divided by number of transactions for each entity type."
}

Question: "What is the most used anticipation method by businesses?"
Response: {
    "metric": "transactions",
    "aggregation": "sum",
    "group_by": ["anticipation_method"],
    "filters": {"entity": "PJ"},
    "sort_by": "metric",
    "sort_order": "desc",
    "limit": 1,
    "explanation": "Finding the preferred anticipation method for business entities (PJ). Counting total transactions by anticipation method, filtered to only include business transactions."
}

Question: "What was the TPV for the last 3 days?"
Response: {
    "metric": "tpv",
    "aggregation": "sum",
    "group_by": ["day"],
    "filters": {},
    "sort_by": "day",
    "sort_order": "desc",
    "limit": 3,
    "explanation": "Showing TPV for the most recent 3 days in the dataset. Grouping by day, sorting by date descending to get the latest days first."
}

IMPORTANT: Return ONLY the JSON object, no additional text."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize the LLM handler.

        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self.model = model
        self.client = OpenAI(api_key=api_key)

    def parse_question(self, question: str) -> Dict[str, Any]:
        """Convert natural language question to structured query intent.

        Args:
            question: User's natural language question

        Returns:
            Dictionary with query intent structure

        Raises:
            Exception: If LLM response cannot be parsed
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content.strip()
            query_intent = json.loads(content)

            self._validate_query_intent(query_intent)

            return query_intent

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {e}")

    def _validate_query_intent(self, intent: Dict[str, Any]) -> None:
        """Validate that the query intent has required fields.

        Args:
            intent: Query intent dictionary

        Raises:
            ValueError: If required fields are missing or invalid
        """
        required_fields = ['metric', 'aggregation', 'group_by', 'filters', 'explanation']

        for field in required_fields:
            if field not in intent:
                raise ValueError(f"Missing required field in query intent: {field}")

        valid_metrics = ['tpv', 'average_ticket', 'transactions', 'merchants']
        if intent['metric'] not in valid_metrics:
            raise ValueError(f"Invalid metric: {intent['metric']}")

        valid_aggregations = ['sum', 'mean', 'count']
        if intent['aggregation'] not in valid_aggregations:
            raise ValueError(f"Invalid aggregation: {intent['aggregation']}")

        if not isinstance(intent['group_by'], list):
            raise ValueError("group_by must be a list")

        if not isinstance(intent['filters'], dict):
            raise ValueError("filters must be a dictionary")
