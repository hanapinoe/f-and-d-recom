import re
from typing import Dict, List

class RecommendationAgent:
    """
    Recommendation Agent: Apply thresholding mechanism and conditionally generate reasoning
    Based on new baseline: 
    - If score is LOWER than threshold: Return the highest scoring dish only
    - If score is HIGHER than threshold: Generate reasoning for the dish
    """
    def __init__(self, llm, threshold: float = 0.5):
        self.llm = llm
        self.threshold = threshold  # Score threshold for decision making
        
    def generate_recommendations(self, dishes: List[Dict], user_query: Dict) -> List[Dict]:
        if not dishes:
            return []
        highest_dish = max(dishes, key=lambda x: x["score"])
        if highest_dish["score"] < self.threshold:
            # Chỉ trả về tên món + giải thích cơ bản
            return [{
                "food_drink_name": highest_dish["item_name"],
                "explanation": "Đây là món có điểm cao nhất trong kết quả tìm kiếm.",
                "score": highest_dish["score"],
                "threshold_status": "lower"
            }]
        else:
            reasoning_prompt = (
                f"- Yêu cầu: Context: {user_query.get('context','')}, "
                f"Health: {user_query.get('health','')}, Taste: {user_query.get('taste','')}\n"
                f"- Món đề xuất: {highest_dish['item_name']}\n"
                f"Hãy giải thích NGẮN GỌN TRONG 1 CÂU tại sao món này phù hợp với người dùng."
            )
            try:
                reason_response = self.llm.complete(reasoning_prompt)
                raw_text = reason_response.text
                import re
                match = re.search(r"(?<=\*\*Giải thích).*?:\s*(.*)", raw_text)
                reason = match.group(1).strip() if match else raw_text.split('---')[0].strip()
                expl = reason
            except Exception:
                expl = "Món này phù hợp với yêu cầu của bạn."
            return [{
                "food_drink_name": highest_dish["item_name"],
                "explanation": expl,
                "score": highest_dish["score"],
            }]
        