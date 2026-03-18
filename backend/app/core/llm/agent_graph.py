import polars as pl
from groq import Groq
from app.config import settings
from app.core.llm.prompt_templates import SYSTEM_PROMPT, DATA_SUMMARY_TEMPLATE
from app.core.llm.tool_registry import register_df
from app.utils.logger import get_logger

logger = get_logger(__name__)

client = Groq(api_key=settings.GROQ_API_KEY)


def run_agent(question: str, df: pl.DataFrame, schema_info: str) -> str:
    register_df("current", df)

    sample = df.head(5).to_pandas().to_string(index=False)
    missing_cols = [col for col in df.columns if df[col].null_count() > 0]

    prompt = DATA_SUMMARY_TEMPLATE.format(
        schema=schema_info,
        sample=sample,
        rows=df.shape[0],
        columns=df.shape[1],
        dqi_score="N/A",
        dqi_grade="N/A",
        missing_cols=", ".join(missing_cols) if missing_cols else "None",
        outlier_cols="See profiling endpoint",
        question=question,
    )

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        # Fallback to Ollama
        from app.core.llm.ollama_client import OllamaClient
        ollama = OllamaClient()
        return ollama.chat(prompt)
