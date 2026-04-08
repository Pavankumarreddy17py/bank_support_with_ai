# Bank Support AI

This repository contains a scaffold for an AI-powered bank support system (backend, frontend, models, and tests).

Quickstart (backend)

1. Create virtual environment and install dependencies:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Run backend:

   uvicorn backend.app:app --reload --port 8000

Frontend

- Frontend scaffold is created using Vite + React. To run it:

  cd frontend
  npm install
  npm run dev

Notes / Next steps

- Add real datasets to `data/kaggle/`
- Implement production authentication (OAuth/JWT)
- Add CI, unit tests and model training pipelines
- Add Docker compose for multi-service setup
