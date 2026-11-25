from ai_agent.database import get_delivery_review_analysis

result = get_delivery_review_analysis()

print("\nDELIVERY VS CUSTOMER REVIEW ANALYSIS")
print("=" * 45)

for item in result:
    print(item)