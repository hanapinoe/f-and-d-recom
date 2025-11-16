from typing import Dict, Any
from src.Coordinator import CoordinatorAgent
from src.Information import InformationAgent
from src.Recommendation import RecommendationAgent


class FoodRecommendationWorkflow:
    """
    Workflow xử lý yêu cầu gợi ý món ăn từ người dùng
    1. Coordinator Agent: Phân tích yêu cầu người dùng thành JSON có cấu tr
    2. Information Agent: Dựa trên JSON đã phân tích để truy xuất danh sách món ăn từ vector store
    3. Recommendation Agent: Áp dụng ngưỡng để quyết định trả về món ăn đề xuất và giải thích (nếu có)

    """

    def __init__(self, llm, vector_store_index, retriever, threshold: float = 0.5):
        self.coordinator = CoordinatorAgent(llm)
        self.information_agent = InformationAgent(vector_store_index, retriever)
        self.recommendation_agent = RecommendationAgent(llm, threshold=threshold)
        self.threshold = threshold

    def process_user_request(
        self, user_input: str, num_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        Hoàn thành quy trình làm việc xử lý yêu cầu của người dùng theo new baseline

        Flow:
        1. Coordinator: Parse user prompt to JSON
        2. Information Agent: Analyze JSON and retrieve top-K dishes
        3. Recommendation Agent: Apply thresholding
           - If highest score < threshold: Return dish with highest score only
           - If highest score >= threshold: Generate reasoning and return dish + reason

        Args:
            user_input: Thuần văn đầu vào của người dùng
            num_recommendations: Số lượng đề xuất món ăn để xem xét (k dishes)

        Returns:
            Bản dict chứa đề xuất cuối cùng với phần giải thích (nếu có)
        """
        try:
            print("[Workflow] Bắt đầu xử lý user_input:", user_input)
            parsed_query = self.coordinator.parse_user_query(user_input)
            print("[Workflow] Parsed query:", parsed_query)
            dish_list = self.information_agent.retrieve_dishes(
                context=parsed_query.get("context", ""),
                health=parsed_query.get("health", ""),
                taste=parsed_query.get("taste", ""),
                k=num_recommendations,
            )
            print("[Workflow] Dish list:", dish_list)
            final_recommendations = self.recommendation_agent.generate_recommendations(
                dishes=dish_list, user_query=parsed_query
            )
            print("[Workflow] Final recommendations:", final_recommendations)
            return {
                "parsed_query": parsed_query,
                "candidate_dishes": dish_list,
                "suggestions": final_recommendations,
                "threshold": self.threshold,
                "status": "success",
            }
        except Exception as e:
            print("[Workflow] Error:", str(e))
            return {"error": str(e), "status": "error"}
