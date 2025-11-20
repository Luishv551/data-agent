"""LLM handler for converting natural language to query intents."""

import os
import json
from typing import Dict, Any, Optional
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
    "explanation": "Brief explanation of what you understood"
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
    "explanation": "Calculate total TPV for each product and return the highest"
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
    "explanation": "Calculate TPV grouped by day of week to show influence"
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
    "explanation": "Calculate average ticket for PF vs PJ entities"
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
    "explanation": "Count transactions by anticipation method for businesses (PJ)"
}

IMPORTANT: Return ONLY the JSON object, no additional text."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """Initialize the LLM handler.

        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

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

            content = response.content.strip() if hasattr(response, 'content') else response.choices[0].message.content.strip()
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
