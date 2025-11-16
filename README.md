# Food & Drink Recommendation Demo

## Overview
This is a demo project for an AI-powered food and drink recommendation system using LlamaIndex, HuggingFace, and large language models.  
The project supports inference with fine-tuned models and provides both FastAPI and Streamlit interfaces.

## Requirements
- Python 3.10+
- GPU (recommended)
- All packages listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/hanapinoe/f-and-d-recom.git
   cd f-and-d-recom
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set your Hugging Face token as an environment variable:
   ```
   set HF_TOKEN=your_hf_token_here
   ```

## Usage
- **Run FastAPI server:**
  ```
  uvicorn api.main:app --reload
  ```
- **Run Streamlit UI:**
  ```
  streamlit run ui/app.py
  ```

## Notes
- Do not push models, real data, or tokens to GitHub.
- Store configuration and secrets in `.env` files or environment variables.

## License
MIT

---

*Feel free to edit this README to better fit your project details!*
