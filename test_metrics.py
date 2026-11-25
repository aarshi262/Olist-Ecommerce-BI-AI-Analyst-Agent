
from ai_agent.database import get_business_metrics

metrics = get_business_metrics()

print("\n===== OLIST BUSINESS METRICS =====")

for key, value in metrics.items():
    print(f"{key}: {value}")
