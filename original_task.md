Context
Using this dataset of CloudWalk transactions (CSV) and must build a local agent (CLI, web app, or “appified” notebook) capable of answering business questions in natural language using a language model (ChatGPT, Claude, Grok, DeepSeek, Llama/Ollama, etc.).

 

Fields
day


entity (individual or business)


product


price_tier


anticipation_method


nitro_or_d0


payment_method


installments


amount_transacted (BRL)


quantity_transactions


quantity_of_merchants


 

Task
Create an agent that:

Understands natural language questions and converts them into queries (SQL or equivalent pipeline) to compute:


Business KPIs
TPV (Total Payment Volume): sum of amount_transacted.


Allow visualization and querying of TPV segmented by entity, product, and payment_method.


Enable product comparison by TPV.


Average Ticket: amount_transacted / quantity_transactions.


Allow visualization and querying by entity, product, and payment_method.


Transactional Insights
Installments: analyze their impact on volume/transaction metrics.


Price Tier: compare performance differences (volume/transactions).


 

Expected Questions
Which product has the highest TPV?


How do weekdays influence TPV?


Which segment has the highest average TPV? And the highest Average Ticket?


Which anticipation method is most used by individuals and by businesses?


(Optional) Automatically generate visualizations from the question (bar, line, boxplot, etc.).

(Optional) Display the generated SQL query (or logic) and a textual reasoning summary.


Automation Proposal
Include or describe a module that generates daily KPIs and automatic alerts, containing:

Daily TPV summary with variation vs D-1, D-7, D-30.


Automatic alerts when:


TPV or Average Ticket is significantly lower in any segment compared to historical averages (e.g., drop > X% or z-score < -2).


Example messages:

“TPV of Product A fell -18% vs 14-day average and -12% vs D-7; largest drop in payment_method = credit.”


“Average Ticket in businesses rose +9% vs D-30; main contribution from product = POS.”


 

Deliverables
Repository (GitHub or ZIP) containing:

Agent code + execution instructions (README).


Example questions and answers (with screenshots).


(Optional) Automated alert module.


Short presentation (README or slides) including:

Context, methodology, and architecture.


Screenshots of visualizations and sample queries.


Explanation of how the agent was built (stack, flow, technical decisions).


Suggested Stack
Language: Python, JS/TS, Go, etc.


LLMs: OpenAI, Anthropic, xAI, DeepSeek, Llama/Ollama.


NL → SQL: LangChain, LlamaIndex, SQLite-utils, Few-shot prompting.


Charts: Matplotlib, Plotly, Vega-Lite, Chart.js.


App: CLI, Streamlit, FastAPI, Next.js, Textual.


Scheduling: cron, APScheduler.


Evaluation Criteria
Data accuracy


Quality of NL→SQL understanding


Clarity of visualizations


Relevance of business insights


Automation and alert functionality


Code organization and architecture


Creativity and robustness