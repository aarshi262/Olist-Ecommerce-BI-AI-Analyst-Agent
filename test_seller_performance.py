
from ai_agent.database import get_seller_delivery_performance

results = get_seller_delivery_performance()

print("\n===== TOP 10 SELLERS WITH HIGHEST LATE DELIVERY =====")

for seller in results:
    print("\nSeller ID:", seller["seller_id"])
    print("Total Orders:", seller["total_orders"])
    print("Late Orders:", seller["late_orders"])
    print("Late Delivery %:", seller["late_delivery_percentage"])
    print("--------------------------------------")
