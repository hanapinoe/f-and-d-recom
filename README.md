# Food & Drink Recommendation Web Demo

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
  uvicorn api.web_demo_api:app --reload
  ```
- **Run Streamlit UI:**
  ```
  streamlit run .\demo\web_demo.py (--server.headless true -> add this prompt if you do not want to auto-start this demo on your browser) 
  ```

## Notes
- Do not push models, real data, or tokens to GitHub.
- Store configuration and secrets in `.env` files or environment variables.

## License
MIT

---
