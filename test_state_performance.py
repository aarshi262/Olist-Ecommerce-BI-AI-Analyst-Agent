
from ai_agent.database import get_state_delivery_performance

results = get_state_delivery_performance()

print("\n===== STATE-WISE DELIVERY PERFORMANCE =====")

for state in results:
    print("\nSeller State:", state["seller_state"])
    print("Total Orders:", state["total_orders"])
    print("Late Orders:", state["late_orders"])
    print("Late Delivery %:", state["late_delivery_percentage"])
    print("--------------------------------------")
