# {{folder_name}}

FastAPI + React Stack project initialized by Scripty

## Project Structure

{{folder_name}}/

- backend/ # FastAPI Python backend
- frontend/ # React TypeScript frontend

## Getting Started

1. Start the backend:
   cd backend

   # If using Poetry:

   poetry install
   poetry run uvicorn main:app --reload

   # If using pip:

   pip install -r requirements.txt
   uvicorn main:app --reload

2. Start the frontend:
   cd frontend
   bun install
   bun run dev

## Features

- Interactive API docs at http://localhost:8000/docs
- React Query for data fetching
- TailwindCSS for styling
- TypeScript for type safety
