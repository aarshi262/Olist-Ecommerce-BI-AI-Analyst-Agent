from ai_agent.database import (
    get_business_metrics,
    get_seller_delivery_performance,
    get_state_delivery_performance,
    get_customer_review_analysis,
    get_delivery_review_analysis
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests


app = FastAPI(
    title="Olist AI Analyst Agent",
    description="AI-powered E-commerce Business Analyst",
    version="1.0.0"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Olist AI Analyst Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

   

    try:
        metrics = get_business_metrics()
        seller_performance = get_seller_delivery_performance()
        state_performance = get_state_delivery_performance()
        customer_reviews = get_customer_review_analysis()
        delivery_reviews = get_delivery_review_analysis()

        delivery_review_summary = {}

        for item in delivery_reviews:
            delivery_review_summary[item["delivery_status"]] = {
                "total_reviews": item["total_reviews"],
                "average_review_score": item["average_review_score"],
                "low_rated_reviews": item["low_rated_reviews"],
                "low_rating_percentage": item["low_rating_percentage"]
            }

        late_delivery_percentage = round(
            (
                metrics["late_orders"] /
                metrics["total_delivered_orders"]
            ) * 100,
            2
        ) if metrics["total_delivered_orders"] else 0

        total_reviews = customer_reviews["total_reviews"]

        for item in customer_reviews["review_score_distribution"]:
            item["percentage"] = round(
                (item["total_reviews"] / total_reviews) * 100,
                2
            ) if total_reviews else 0

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {error}"
        )


    top_5_sellers = sorted(
        seller_performance,
        key=lambda seller: seller["late_delivery_percentage"],
        reverse=True
    )[:5]

    top_5_states = sorted(
        state_performance,
        key=lambda state: state["late_delivery_percentage"],
        reverse=True
    )[:5]

    
    business_insights = {}

    if seller_performance:
        business_insights["highest_late_delivery_seller"] = max(
            seller_performance,
            key=lambda seller: seller["late_delivery_percentage"]
        )

    if state_performance:
        business_insights["highest_late_delivery_state"] = max(
            state_performance,
            key=lambda state: state["late_delivery_percentage"]
        )

        business_insights["highest_order_volume_state"] = max(
            state_performance,
            key=lambda state: state["total_orders"]
        )

    seller = business_insights.get(
        "highest_late_delivery_seller", {}
    )

    late_state = business_insights.get(
        "highest_late_delivery_state", {}
    )

    volume_state = business_insights.get(
        "highest_order_volume_state", {}
    )

    late_review = delivery_review_summary.get(
        "Late Delivery", {}
    )

    ontime_review = delivery_review_summary.get(
        "On-Time Delivery", {}
    )

    

    recommendations = [
        (
            f"Monitor the seller with the highest observed late "
            f"delivery rate ({seller.get('seller_id', 'N/A')}). "
            "Review order fulfillment regularly and create a "
            "performance improvement plan."
        ),
        (
            f"Investigate delivery operations associated with "
            f"seller state {late_state.get('seller_state', 'N/A')}, "
            f"which has a late delivery rate of "
            f"{late_state.get('late_delivery_percentage', 'N/A')}%. "
            "Review delivery timelines and identify operational "
            "bottlenecks using order-level records."
        ),
        (
            f"Prioritize delivery capacity monitoring in "
            f"seller state {volume_state.get('seller_state', 'N/A')}, "
            f"which has {volume_state.get('total_orders', 'N/A')} "
            "orders in the analyzed data."
        ),
        (
            f"Improve customer communication for delayed orders. "
            f"Late-delivery reviews have an average rating of "
            f"{late_review.get('average_review_score', 'N/A')}, "
            f"compared with "
            f"{ontime_review.get('average_review_score', 'N/A')} "
            "for on-time deliveries."
        ),
        (
            "Introduce an early-warning process that compares "
            "actual delivery progress with estimated delivery dates. "
            "Escalate orders at risk of missing their estimated "
            "delivery date."
        )
    ]

    recommendations_text = "\n".join(
        f"{i}. {item}"
        for i, item in enumerate(recommendations, start=1)
    )

    

    verified_findings = f"""
VERIFIED BUSINESS FINDINGS

HIGHEST LATE-DELIVERY SELLER
(Among Returned Top 10 Sellers)

Seller ID: {seller.get('seller_id', 'N/A')}
Total Orders: {seller.get('total_orders', 'N/A')}
Late Orders: {seller.get('late_orders', 'N/A')}
Late Delivery Percentage: {seller.get('late_delivery_percentage', 'N/A')}%

HIGHEST LATE-DELIVERY SELLER STATE

Seller State Code: {late_state.get('seller_state', 'N/A')}
Total Orders: {late_state.get('total_orders', 'N/A')}
Late Orders: {late_state.get('late_orders', 'N/A')}
Late Delivery Percentage: {late_state.get('late_delivery_percentage', 'N/A')}%

HIGHEST ORDER-VOLUME SELLER STATE

Seller State Code: {volume_state.get('seller_state', 'N/A')}
Total Orders: {volume_state.get('total_orders', 'N/A')}
Late Orders: {volume_state.get('late_orders', 'N/A')}
Late Delivery Percentage: {volume_state.get('late_delivery_percentage', 'N/A')}%

OVERALL DELIVERY PERFORMANCE

Total Delivered Orders: {metrics['total_delivered_orders']}
Late Orders: {metrics['late_orders']}
Late Delivery Percentage: {late_delivery_percentage}%

CUSTOMER REVIEW ANALYSIS

Total Reviews: {customer_reviews['total_reviews']}
Average Review Score: {customer_reviews['average_review_score']}
Low-Rated Reviews: {customer_reviews['low_rated_reviews']}
Low-Rating Percentage: {customer_reviews['low_rating_percentage']}%

DELIVERY-WISE CUSTOMER SATISFACTION

{delivery_review_summary}

BUSINESS RECOMMENDATIONS

{recommendations_text}
"""

    

    system_prompt = f"""
You are an e-commerce business analyst.

You must answer using ONLY the verified database findings below.

VERIFIED DATABASE DATA:

{verified_findings}

ADDITIONAL DATABASE DATA:

Business Metrics: {metrics}

Seller Performance: {seller_performance}

State Performance: {state_performance}

Customer Review Analysis: {customer_reviews}

Delivery Review Analysis: {delivery_review_summary}

STRICT RULES:

1. Never invent numerical values.

2. Never invent delivery delay reasons.

3. Never invent weather problems, inventory shortages,
   shipping problems or operational causes.

4. Do not assume information that is not present in the database.

5. Seller state means the seller's location, not the customer's location.

6. Refer to MA, SP and other values as seller state codes.
   Do not guess or invent their geographic meaning.

7. Do not describe overall average delivery days as
   a state-specific average.

8. The overall average delivery time is
   {metrics['average_delivery_days']} days.
   It is not a state-specific metric.

9. Seller performance contains only the returned top 10 sellers.
   Do not claim that these represent every seller.

10. Review counts and order counts are different.
    Never mix them.

11. Late Delivery review findings:
    7700 reviews, average score 2.57,
    4160 low-rated reviews, 54.03%.

12. On-Time Delivery review findings:
    88653 reviews, average score 4.29,
    8186 low-rated reviews, 9.23%.

13. Low-rated reviews mean review scores of 1 and 2 only.

14. Do not claim that late delivery causes low ratings.
    Describe the observed association only.

15. When recommendations are requested,
    use exactly the five verified Python-generated
    recommendations provided above.

16. If the database does not contain requested information,
    clearly say that the information is unavailable.

17. Use professional language and clear headings.

18. Freight values are in Brazilian Real (R$).

19. Answer only what the user has asked.
"""



    question_lower = request.question.lower()

    is_state_late_question = (
        "state" in question_lower
        and "late" in question_lower
        and any(
            word in question_lower
            for word in ["highest", "maximum", "max"]
        )
    )

    is_customer_satisfaction_question = (
        (
            "customer satisfaction" in question_lower
            or "customer review" in question_lower
            or "review" in question_lower
            or "rating" in question_lower
        )
        and "late" in question_lower
        and (
            "on-time" in question_lower
            or "on time" in question_lower
            or "ontime" in question_lower
        )
    )

    is_seller_late_question = (
        "seller" in question_lower
        and "state" not in question_lower
        and "late" in question_lower
        and any(
            word in question_lower
            for word in ["highest", "maximum", "max"]
        )
    )

    is_overall_business_question = (
        "overall" in question_lower
        and (
            "business" in question_lower
            or "performance" in question_lower
        )
    )

    response_source = "ollama"

    

    if is_state_late_question and late_state:

        response_source = "database"

        ai_answer = (
            f"Based on the actual PostgreSQL database findings, "
            f"the seller state with the highest late delivery "
            f"percentage is {late_state['seller_state']}.\n\n"

            f"**Verified Performance:**\n\n"
            f"- Seller State Code: {late_state['seller_state']}\n"
            f"- Total Orders: {late_state['total_orders']}\n"
            f"- Late Orders: {late_state['late_orders']}\n"
            f"- Late Delivery Percentage: "
            f"{late_state['late_delivery_percentage']}%\n\n"

            f"**Performance Analysis:**\n\n"
            f"{late_state['late_orders']} out of "
            f"{late_state['total_orders']} orders associated "
            f"with seller state {late_state['seller_state']} "
            f"were delivered late.\n\n"

            f"This is the highest late delivery percentage "
            f"among the seller states returned by the database "
            f"analysis.\n\n"

            f"**Business Insight:**\n\n"
            f"Seller state {late_state['seller_state']} should be "
            f"prioritized for further delivery-performance "
            f"investigation. The available database findings do "
            f"not establish the specific reasons for these delays."
        )

    

    elif is_seller_late_question and seller:

        response_source = "database"

        ai_answer = (
            "**Highest Late-Delivery Seller Analysis**\n\n"

            "Based on the actual PostgreSQL database findings, "
            "the seller with the highest observed late-delivery "
            "percentage among the returned top 10 sellers is:\n\n"

            f"- Seller ID: {seller['seller_id']}\n"
            f"- Total Orders: {seller['total_orders']}\n"
            f"- Late Orders: {seller['late_orders']}\n"
            f"- Late Delivery Percentage: "
            f"{seller['late_delivery_percentage']}%\n\n"

            "**Performance Analysis**\n\n"

            f"This seller had {seller['late_orders']} late orders "
            f"out of {seller['total_orders']} total orders. "
            f"The resulting late-delivery rate is "
            f"{seller['late_delivery_percentage']}%.\n\n"

            "**Business Insight**\n\n"

            "This seller should be prioritized for further "
            "delivery-performance investigation. The available "
            "database findings do not establish the specific "
            "reasons for these delays.\n\n"

            "Note: This is the highest rate among the returned "
            "top 10 seller results, not necessarily every seller "
            "in the database. Seller-state percentages are "
            "different from individual seller percentages."
        )

    

    elif is_customer_satisfaction_question and late_review and ontime_review:

        response_source = "database"

        ai_answer = (
            "**Customer Satisfaction: Late vs On-Time Deliveries**\n\n"

            "**1. Average Review Rating**\n\n"
            f"- Late Delivery: {late_review['average_review_score']} / 5\n"
            f"- On-Time Delivery: {ontime_review['average_review_score']} / 5\n\n"

            "On-time deliveries have a higher average review rating "
            "than late deliveries.\n\n"

            "**2. Number of Reviews**\n\n"
            f"- Late Delivery: {late_review['total_reviews']:,} reviews\n"
            f"- On-Time Delivery: {ontime_review['total_reviews']:,} reviews\n\n"

            "**3. Low-Rated Reviews (1 or 2 Stars)**\n\n"
            f"- Late Delivery: {late_review['low_rated_reviews']:,} "
            f"({late_review['low_rating_percentage']}%)\n"
            f"- On-Time Delivery: {ontime_review['low_rated_reviews']:,} "
            f"({ontime_review['low_rating_percentage']}%)\n\n"

            "**Key Findings**\n\n"

            f"1. Late deliveries have an average rating of "
            f"{late_review['average_review_score']}, compared with "
            f"{ontime_review['average_review_score']} for on-time deliveries.\n\n"

            f"2. The low-rating percentage is "
            f"{late_review['low_rating_percentage']}% for late deliveries "
            f"and {ontime_review['low_rating_percentage']}% for on-time deliveries.\n\n"

            f"3. There are {late_review['low_rated_reviews']:,} low-rated "
            f"reviews among late deliveries and "
            f"{ontime_review['low_rated_reviews']:,} among on-time deliveries.\n\n"

            "4. Percentages provide a useful comparison because the "
            "number of reviews differs between the two groups.\n\n"

            "5. The observed data shows an association between delivery "
            "status and customer ratings. It does not establish causation.\n\n"

            "**Exactly Five Practical Improvements**\n\n"

            "1. **Introduce Early Delivery Alerts:** Monitor order progress "
            "against estimated delivery dates and flag orders that may be late.\n\n"

            "2. **Improve Customer Communication:** Send timely updates "
            "when an order is delayed and provide revised estimates when available.\n\n"

            "3. **Review Late-Delivery Orders:** Examine delayed orders "
            "to identify where delivery timelines are being missed.\n\n"

            "4. **Monitor Customer Feedback:** Track average ratings and "
            "the percentage of 1- and 2-star reviews separately.\n\n"

            "5. **Set Delivery Performance Targets:** Monitor late-delivery "
            "rates over time and review progress regularly.\n\n"

            "**Conclusion**\n\n"

            "The database findings show that on-time deliveries are "
            "associated with better customer ratings. The observed "
            "relationship does not establish that delivery status alone "
            "caused the difference."
        )

    

    elif is_overall_business_question:

        response_source = "database"

        ai_answer = (
            "**Overall Business Performance Summary**\n\n"

            "**1. Order and Delivery Performance**\n\n"
            f"- Total Delivered Orders: "
            f"{metrics['total_delivered_orders']:,}\n"
            f"- Late Orders: {metrics['late_orders']:,}\n"
            f"- Late Delivery Percentage: "
            f"{late_delivery_percentage}%\n"
            f"- Average Delivery Time: "
            f"{metrics['average_delivery_days']} days\n\n"

            "**2. Freight Performance**\n\n"
            f"- Average Freight per Order: "
            f"R$ {metrics['average_freight_per_order']}\n\n"

            "**3. Customer Satisfaction**\n\n"
            f"- Total Reviews: {customer_reviews['total_reviews']:,}\n"
            f"- Average Review Score: "
            f"{customer_reviews['average_review_score']} / 5\n"
            f"- Low-Rated Reviews: "
            f"{customer_reviews['low_rated_reviews']:,}\n"
            f"- Low-Rating Percentage: "
            f"{customer_reviews['low_rating_percentage']}%\n\n"

            "**4. Delivery-wise Customer Satisfaction**\n\n"
            f"- Late Delivery Average Rating: "
            f"{late_review.get('average_review_score', 'N/A')} / 5\n"
            f"- On-Time Delivery Average Rating: "
            f"{ontime_review.get('average_review_score', 'N/A')} / 5\n\n"

            "**5. Exactly Five Business Recommendations**\n\n"
            f"{recommendations_text}\n\n"

            "**Conclusion**\n\n"
            "The database findings show that overall late delivery "
            f"stands at {late_delivery_percentage}%, while the average "
            f"customer review score is "
            f"{customer_reviews['average_review_score']} out of 5. "
            "Delivery monitoring and customer satisfaction should "
            "remain important operational priorities.\n\n"

            "Note: Revenue and total freight are not included because "
            "these metrics are not currently provided by the verified "
            "business metrics function."
        )

    

    else:

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": request.question
                }
            ],
            "stream": False
        }

        try:
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            result = response.json()

            ai_answer = result.get(
                "message", {}
            ).get("content")

            if not ai_answer or not ai_answer.strip():
                raise HTTPException(
                    status_code=503,
                    detail="Ollama returned an empty response."
                )

        except requests.RequestException as error:
            raise HTTPException(
                status_code=503,
                detail=f"Ollama connection failed: {error}"
            )

        except ValueError as error:
            raise HTTPException(
                status_code=503,
                detail=f"Invalid Ollama response: {error}"
            )


    return {
        "question": request.question,
        "answer": ai_answer,
        "response_source": response_source,
        "verified_findings": verified_findings,
        "business_metrics": metrics,
        "actual_late_delivery_percentage": float(
            late_delivery_percentage
        ),
        "seller_performance": seller_performance,
        "top_5_sellers": top_5_sellers,
        "state_performance": state_performance,
        "top_5_states": top_5_states,
        "customer_review_analysis": customer_reviews,
        "delivery_review_analysis": delivery_reviews,
        "delivery_review_summary": delivery_review_summary,
        "business_insights": business_insights,
        "recommendations": recommendations,
        "model": MODEL_NAME
    }
