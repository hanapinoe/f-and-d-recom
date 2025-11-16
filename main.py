# from services import setup_workflow

def choose_model(llm_choice: int) -> str:
     """
     Chọn mô hình LLM dựa trên lựa chọn của người dùng
     
     Args:
          llm_choice: Số nguyên đại diện cho lựa chọn mô hình

     Returns:
          Chuỗi tên mô hình LLM
     """
     model_dict = {
          1: "Qwen/Qwen2.5-1.5B",
          2: "ura-hcmut/GemSUra-2B",
     }
     return model_dict.get(llm_choice, "None")

     
# Menu tương tác với người dùng
def menu():
     while True: # Vòng lặp chính của menu
          print("=== HỆ THỐNG GỢI Ý ĐỒ ĂN/THỨC UỐNG CÁ NHÂN HÓA ===")
          print("1. Gợi ý Đồ ăn/Thức uống")
          print("0. Thoát")
          try:
               choose = int(input("Chọn chức năng: "))
               if choose == 1:
                    while True:
                         try: 
                              print("--- Chọn Mô hình Ngôn ngữ Lớn (LLM) ---")
                              print("1. Qwen2.5-1.5B")
                              print("2. GemSUra-2B")
                              print("Khác. Không chọn model (quay lại menu chính)")
                              llm_choice = int(input("Chọn mô hình LLM: "))
                              model_name = choose_model(llm_choice)
                              if model_name == "None":
                                   print("Quay lại menu chính. \n")
                                   break
                              else:
                                   print(f"Bạn đã chọn mô hình: {model_name}")
                                   print("!Lưu ý: Prompt cần phải có 3 yếu tố: Tình trạng sức khỏe, Khẩu vị, Ngữ cảnh.")
                                   user_input = input("Nhập yêu cầu của bạn về Đồ ăn/Thức uống: ")
                                   # Đóng băng workflow, chỉ in ra dữ liệu mẫu
                                   print("Kết quả gợi ý Đồ ăn/Thức uống:")
                                   print({
                                        "parsed_query": {
                                             "context": "Buổi tối, muốn uống nước trái cây ngọt",
                                             "health": "Bình thường",
                                             "taste": "Ngọt"
                                        }
                                   })
                                   print({"suggestions": [
                                             {
                                                  "item_id": "123",
                                                  "item_name": "Nước ép cam",
                                                  "score": 0.95
                                             },
                                             {
                                                  "item_id": "456",
                                                  "item_name": "Sinh tố dâu",
                                                  "score": 0.89
                                             }
                                        ]
                                   })
                                   print()
                         except ValueError:
                              print("!Vui lòng nhập một số nguyên hợp lệ. \n")
               elif choose == 0:
                    print("CẢM ƠN VÀ HẸN GẶP LẠI !")
                    break
               else:
                    print("!Lựa chọn không hợp lệ. Vui lòng thử lại \n.")
          except ValueError:
               print("!Vui lòng nhập một số nguyên hợp lệ. \n")


def main():
     return None

if __name__ == "__main__":
     menu()