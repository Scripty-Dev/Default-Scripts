# {{folder_name}}

A Flask + React application with TypeScript and TailwindCSS.

## Project Structure

```
{{folder_name}}/
├── backend/           # Flask backend
│   ├── app/           # Flask application
│   │   ├── routes/    # API routes
│   │   ├── models/    # Database models
│   │   └── schemas/   # Marshmallow schemas
│   ├── pyproject.toml # Poetry configuration
│   └── .env           # Environment variables
└── frontend/          # React frontend
    ├── src/           # React source code
    ├── public/        # Static assets
    └── package.json   # Frontend dependencies
```

## Getting Started

### Backend Setup

```bash
cd backend
poetry install
poetry run flask run
```

### Frontend Setup

```bash
cd frontend
bun install
bun run dev
```

## Features

- Flask backend with SQLAlchemy ORM
- React frontend with TypeScript
- TailwindCSS for styling
- API integration between frontend and backend
