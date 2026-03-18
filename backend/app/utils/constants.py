SUPPORTED_FORMATS = [".csv", ".xlsx", ".json", ".parquet"]
DQI_WEIGHTS = {"completeness": 0.4, "uniqueness": 0.2, "consistency": 0.2, "outlier": 0.2}
DOMAIN_KEYWORDS = {
    "retail": ["sales", "revenue", "product", "sku", "order", "customer"],
    "finance": ["amount", "balance", "transaction", "debit", "credit", "account"],
    "healthcare": ["patient", "diagnosis", "icd", "medication", "dosage", "admission"],
    "saas": ["mrr", "churn", "subscription", "user", "plan", "trial"],
}
