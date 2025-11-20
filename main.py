"""CloudWalk Data Agent - Natural language interface for business analytics."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_handler import DataHandler
from llm_handler import LLMHandler
from query_executor import QueryExecutor, QueryResult


class DataAgentApp:
    """Streamlit application for the data agent."""

    EXAMPLE_QUESTIONS = [
        "Which product has the highest TPV?",
        "How do weekdays influence TPV?",
        "Which segment has the highest average ticket?",
        "What is the most used anticipation method by businesses?",
        "Compare TPV by payment method",
        "What is the total TPV for credit card transactions?"
    ]

    def __init__(self):
        """Initialize the application."""
        self._initialize_session_state()
        self._initialize_components()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'history' not in st.session_state:
            st.session_state.history = []

    def _initialize_components(self):
        """Initialize data handler, LLM handler, and query executor."""
        try:
            if 'data_handler' not in st.session_state:
                st.session_state.data_handler = DataHandler("transactions.csv")

            if 'llm_handler' not in st.session_state:
                st.session_state.llm_handler = LLMHandler()

            if 'query_executor' not in st.session_state:
                st.session_state.query_executor = QueryExecutor(
                    st.session_state.data_handler
                )

        except Exception as e:
            st.error(f"Initialization error: {e}")
            st.stop()

    def render_header(self):
        """Render application header."""
        st.title("CloudWalk Data Agent")
        st.markdown("Ask questions about your transaction data in natural language")

        with st.expander("Dataset Summary"):
            summary = st.session_state.data_handler.get_data_summary()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows", f"{summary['total_rows']:,}")
                st.metric("Total TPV", f"R$ {summary['total_tpv']:,.2f}")

            with col2:
                st.metric("Date Range", f"{summary['date_range']['start']} to {summary['date_range']['end']}")
                st.metric("Average Ticket", f"R$ {summary['average_ticket']:,.2f}")

            with col3:
                st.metric("Products", summary['unique_products'])
                st.metric("Entities", summary['unique_entities'])

    def render_example_questions(self):
        """Render example question buttons."""
        st.subheader("Example Questions")

        cols = st.columns(3)
        for idx, question in enumerate(self.EXAMPLE_QUESTIONS):
            col = cols[idx % 3]
            with col:
                if st.button(question, key=f"example_{idx}", use_container_width=True):
                    return question

        return None

    def render_question_input(self):
        """Render question input field."""
        st.subheader("Ask Your Question")
        question = st.text_input(
            "Enter your question:",
            placeholder="e.g., Which product has the highest TPV?",
            label_visibility="collapsed"
        )

        return question

    def process_question(self, question: str):
        """Process a user question and display results.

        Args:
            question: User's natural language question
        """
        if not question or not question.strip():
            return

        with st.spinner("Processing your question..."):
            try:
                query_intent = st.session_state.llm_handler.parse_question(question)

                result = st.session_state.query_executor.execute(query_intent)

                self.render_results(question, result)

            except Exception as e:
                st.error(f"Error processing question: {e}")

    def render_results(self, question: str, result: QueryResult):
        """Render query results.

        Args:
            question: Original question
            result: QueryResult object
        """
        st.divider()
        st.subheader("Results")

        st.info(result.explanation)

        if result.metric_value is not None:
            st.metric(
                result.metric_name,
                self._format_metric_value(result.metric_value, result.query_intent['metric'])
            )

        if len(result.data) > 0:
            st.subheader("Data")

            display_df = result.data.copy()
            if 'metric_value' in display_df.columns:
                display_df['metric_value'] = display_df['metric_value'].apply(
                    lambda x: self._format_metric_value(x, result.query_intent['metric'])
                )

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            if len(result.data) > 1 and 'metric_value' in result.data.columns:
                self.render_visualization(result)

        with st.expander("Query Details"):
            st.json(result.query_intent)

    def render_visualization(self, result: QueryResult):
        """Render visualization for results.

        Args:
            result: QueryResult object
        """
        st.subheader("Visualization")

        group_by = result.query_intent.get('group_by', [])

        if not group_by or 'metric_value' not in result.data.columns:
            return

        x_column = group_by[0]
        y_column = 'metric_value'

        if x_column == 'day' or x_column == 'day_of_week':
            if x_column == 'day_of_week':
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                fig = px.bar(
                    result.data,
                    x=x_column,
                    y=y_column,
                    title=f"{result.metric_name} by {x_column}",
                    category_orders={x_column: day_order}
                )
            else:
                fig = px.line(
                    result.data,
                    x=x_column,
                    y=y_column,
                    title=f"{result.metric_name} over time"
                )
        else:
            fig = px.bar(
                result.data,
                x=x_column,
                y=y_column,
                title=f"{result.metric_name} by {x_column}"
            )

        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=result.metric_name,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    def _format_metric_value(self, value: float, metric_type: str) -> str:
        """Format metric value based on type.

        Args:
            value: Metric value
            metric_type: Type of metric

        Returns:
            Formatted string
        """
        if metric_type in ['tpv', 'average_ticket']:
            return f"R$ {value:,.2f}"
        else:
            return f"{int(value):,}"

    def run(self):
        """Run the Streamlit application."""
        st.set_page_config(
            page_title="CloudWalk Data Agent",
            page_icon=":bar_chart:",
            layout="wide"
        )

        self.render_header()

        example_question = self.render_example_questions()

        question = self.render_question_input()

        if example_question:
            self.process_question(example_question)
        elif question:
            self.process_question(question)


def main():
    """Application entry point."""
    app = DataAgentApp()
    app.run()


if __name__ == "__main__":
    main()
