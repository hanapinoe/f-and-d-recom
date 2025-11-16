import json
from typing import Dict


class CoordinatorAgent:
    """
    Coordinator Agent: Format theo cấu trúc định sẵn
    """

    def __init__(self, llm):
        self.llm = llm

    def parse_user_query(self, user_input: str) -> Dict[str, str]:
        """Format input của người dùng theo dạng JSON có cấu trúc định sẵn"""
        print(f"[CoordinatorAgent] Input: {user_input}")
        prompt = f"""
          Bạn là một tác tử điều phối thông minh.
          Người dùng sẽ mô tả những gì họ muốn ăn hoặc uống, bao gồm tâm trạng, tình trạng sức khỏe hoặc khẩu vị.
          Hãy phân tích thông tin thành metadata có cấu trúc dạng JSON với các trường sau:
          
          - "context": bối cảnh, tâm trạng hiện tại và nguyên liệu của ăn (không bao gồm về giác và tình trạng sức khỏe)
          - "health": tình trạng sức khỏe, bệnh lý hoặc hạn chế ăn uống
          - "taste": khẩu vị ưa thích
          
          Không suy luận thêm, chỉ trích xuất từ thông tin họ mô tả.
          Chỉ hiển thị kết quả cuối cùng.
          
          Bây giờ xử lý đầu vào này: {user_input}
          
          Chỉ cho ra JSON 1 lần duy nhất, không thêm bất kì văn bản nào khác.
          """

        try:
            response = self.llm.complete(prompt, format="json")
            output = json.loads(response.text)
            print(f"[CoordinatorAgent] Output: {output}")
            return output
        except:
            fallback_output = {
                "context": user_input,
                "health": "Bình thường",
                "taste": "Không xác nhận",
            }
            print(f"[CoordinatorAgent] Output (fallback): {fallback_output}")
            return fallback_output
