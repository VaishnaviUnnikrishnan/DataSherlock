SYSTEM_PROMPT = """
You are DataSherlock, an expert data analyst AI assistant.
You have access to a dataset and its profiling results.
Answer questions clearly, concisely, and with data-backed reasoning.
When recommending actions, be specific and actionable.
"""

DATA_SUMMARY_TEMPLATE = """
Dataset Schema:
{schema}

Dataset Sample (first 5 rows):
{sample}

Profiling Summary:
- Rows: {rows}, Columns: {columns}
- DQI Score: {dqi_score} ({dqi_grade})
- Missing values detected in: {missing_cols}
- Outliers detected in: {outlier_cols}

User Question: {question}

Provide a clear, analytical answer.
"""

INSIGHT_SUMMARY_TEMPLATE = """
Based on the following data quality and profiling results, generate an executive summary:

DQI Score: {dqi_score} | Grade: {dqi_grade}
Key Issues: {issues}
Strong Correlations: {correlations}
Recommendations: {recommendations}

Write a 3-paragraph executive summary suitable for a non-technical stakeholder.
"""
