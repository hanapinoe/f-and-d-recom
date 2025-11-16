from typing import List, Dict


class InformationAgent:
    """
    Information Agent: Đưa ra K đề xuất món ăn dựa trên truy vấn đã định dạng
    """

    def __init__(self, vector_store_index, retriever):
        self.index = vector_store_index
        self.retriever = retriever

    def retrieve_dishes(
        self, context: str, health: str, taste: str, k: int = 10
    ) -> List[Dict]:
        """Đưa ra đề xuất món ăn dựa trên truy vấn đã định dạng"""
        print(
            f"[InformationAgent] Input: context={context}, health={health}, taste={taste}, k={k}"
        )

        # Format query text for retrieval
        query_text = (
            f"Tình trạng sức khỏe: {health}. Khẩu vị: {taste}. Ngữ cảnh: {context}."
        )

        # Retrieve from vector store
        retrieved_nodes = self.retriever.retrieve(query_text)

        # Format results
        suggestions = []
        for node in retrieved_nodes:
            suggestions.append(
                {
                    "item_id": node.metadata.get("id"),
                    "item_name": node.metadata.get("recommendation"),
                    "score": round(node.score, 3),
                }
            )

        # Remove duplicates and return top K
        unique_suggestions = []
        seen = set()

        for s in suggestions:
            name = s["item_name"].strip().lower()
            if name not in seen and len(unique_suggestions) < k:
                seen.add(name)
                unique_suggestions.append(s)

        print(f"[InformationAgent] Output: {unique_suggestions}")

        return unique_suggestions
