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
        self, user_input: dict, num_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        Hoàn thành quy trình làm việc xử lý yêu cầu của người dùng theo baseline mới

        Quy trình:
        1. Information Agent: Phân tích JSON và truy xuất top-K món ăn
        2. Recommendation Agent: Áp dụng ngưỡng
        - Nếu điểm cao nhất < ngưỡng: Trả về món ăn có điểm cao nhất
        - Nếu điểm cao nhất >= ngưỡng: Sinh giải thích và trả về món ăn + lý do

        args:
            - user_input: {
                "health": tình trạng sức khỏe, bệnh lý hoặc hạn chế ăn uống
                "taste": khẩu vị ưa thích
                "context": bối cảnh, tâm trạng hiện tại và nguyên liệu của ăn (không bao gồm về giác và tình trạng sức khỏe)
            }
            - num_recommendations: Số lượng món ăn đề xuất để xem xét (k món)

        returns:
            Dict chứa đề xuất cuối cùng và phần giải thích (nếu có)
        """
        try:
            # print("[Workflow] Bắt đầu xử lý user_input:", user_input)
            # parsed_query = self.coordinator.parse_user_query(user_input)
            # print("[Workflow] Parsed query:", parsed_query)
            # dish_list = self.information_agent.retrieve_dishes(
            #     context=parsed_query.get("context", ""),
            #     health=parsed_query.get("health", ""),
            #     taste=parsed_query.get("taste", ""),
            #     k=num_recommendations,
            # )
            dish_list = self.information_agent.retrieve_dishes(
                context=user_input.get("context", ""),
                health=user_input.get("health", ""),
                taste=user_input.get("taste", ""),
                k=num_recommendations,
            )
            print("[Workflow] Dish list:", dish_list)
            final_recommendations = self.recommendation_agent.generate_recommendations(
                dishes=dish_list, user_query=user_input
            )
            print("[Workflow] Final recommendations:", final_recommendations)
            return {
                "user_query": user_input,
                "candidate_dishes": dish_list,
                "suggestions": final_recommendations,
                "threshold": self.threshold,
                "status": "success",
            }
        except Exception as e:
            print("[Workflow] Error:", str(e))
            return {"error": str(e), "status": "error"}
