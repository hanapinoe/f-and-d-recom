import streamlit as st

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-left: 48px;
        padding-right: 48px;
    }
    .stTextInput > div > div > input {
        width: 1000px !important;
    }
    .stTable {
        width: 1000px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

import requests


def reset_input():
    st.session_state.user_input = ""
    st.session_state.result_shown = False
    st.session_state.model_name = ""
    st.session_state.data = None
    st.session_state.loading = False
    # Gọi API /reset để backend cũng reset workflow
    try:
        requests.post("http://localhost:8000/reset")
    except Exception:
        pass


# Khởi tạo trạng thái phiên làm việc
for key, value in [
    ("result_shown", False),
    ("health", ""),
    ("taste", ""),
    ("context", ""),
    ("model_name", ""),
    ("data", None),
    ("loading", False),
]:
    if key not in st.session_state:
        st.session_state[key] = value

st.title("Demo hệ thống gợi ý đồ ăn/thức uống cá nhân hóa")

model_choice = st.radio(
    "Chọn mô hình LLM",
    ["Qwen2.5-1.5B", "GemSUra-2B", "Qwen2.5-1.5B_LoRA", "GemSUra-2B_LoRA"],
    disabled=st.session_state.loading,
)

health = st.text_input(
    "Nhập tình trạng sức khỏe (health):",
    value=st.session_state.health,
    disabled=st.session_state.loading,
)
taste = st.text_input(
    "Nhập khẩu vị ưa thích (taste):",
    value=st.session_state.taste,
    disabled=st.session_state.loading,
)
context = st.text_input(
    "Nhập bối cảnh (context):",
    value=st.session_state.context,
    disabled=st.session_state.loading,
)

col1, col2 = st.columns([1, 1])

with col1:
    suggest_btn = st.button("Gợi ý", disabled=st.session_state.loading)
with col2:
    reset_btn = st.button(
        "Nhập yêu cầu mới (reset)",
        on_click=reset_input,
        disabled=not st.session_state.result_shown or st.session_state.loading,
    )

if suggest_btn and not st.session_state.loading:
    if (
        not (str(health or "").strip())
        or not (str(taste or "").strip())
        or not (str(context or "").strip())
    ):
        st.error(
            "Bạn cần nhập thông tin vào các trường health, taste và context để hệ thống xử lý!"
        )
    else:
        st.session_state.loading = True
        st.rerun()

if st.session_state.loading:
    with st.spinner("Đang xử lý..."):
        # Tải lên mô hình tương ứng
        if model_choice == "Qwen2.5-1.5B":
            st.session_state.model_name = "Qwen/Qwen2.5-1.5B"
        elif model_choice == "GemSUra-2B":
            st.session_state.model_name = "ura-hcmut/GemSUra-2B"
        elif model_choice == "Qwen2.5-1.5B_LoRA":
            st.session_state.model_name = (
                "E:/study/AIP_capstone/capstone/models/qwen2-foodanddrink-merged"
            )
        elif model_choice == "GemSUra-2B_LoRA":
            st.session_state.model_name = (
                "E:/study/AIP_capstone/capstone/models/GemSUra-2B_merged"
            )
        # Đóng gói user_input thành dict
        user_input_dict = {
            "health": str(health).strip(),
            "taste": str(taste).strip(),
            "context": str(context).strip(),
        }
        # Tạo payload với định dạng đúng
        payload = {
            "model_name": st.session_state.model_name,
            "user_input": user_input_dict,
        }
        st.session_state.user_input = user_input_dict # Lưu lại để hiển thị sau này

        # Gọi API /recommend
        try:
            response = requests.post("http://localhost:8000/recommend", json=payload)
            if response.status_code == 200:
                st.session_state.data = response.json()
                st.session_state.result_shown = True
                # Cập nhật lại các trường nhập liệu vào session_state
                st.session_state.health = user_input_dict["health"]
                st.session_state.taste = user_input_dict["taste"]
                st.session_state.context = user_input_dict["context"]
            else:
                st.error("API trả về lỗi hoặc không kết nối được.")
        except Exception as e:
            st.error(f"Lỗi khi gọi API: {e}")
        st.session_state.loading = False
        st.rerun()

if st.session_state.result_shown and st.session_state.data:
    st.write(f"Model: {st.session_state.model_name}")
    st.write(
        "Request:",
        {
            "health": st.session_state.health,
            "taste": st.session_state.taste,
            "context": st.session_state.context,
        },
    )
    st.write("Gợi ý món ăn/thức uống:")

    # Làm tròn score và đổi tên cột
    import pandas as pd

    df = pd.DataFrame(st.session_state.data["suggestions"])
    if "score" in df.columns:
        df["score"] = df["score"].apply(lambda x: round(float(x), 2))
        df = df.rename(columns={"score": "Score"})
    st.table(df)
