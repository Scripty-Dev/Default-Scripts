# {{folder_name}}

A full-stack MERN (MongoDB, Express, React, Node.js) application with Next.js frontend.

## Project Structure

```
{{folder_name}}/
├── backend/           # Express + MongoDB backend
│   ├── src/           # Backend source code
│   │   ├── controllers/ # API controllers
│   │   ├── middleware/  # Express middleware
│   │   ├── models/      # Mongoose models
│   │   └── routes/      # API routes
│   ├── package.json   # Backend dependencies
│   └── .env           # Environment variables
└── frontend/          # Next.js frontend
    ├── src/           # Frontend source code
    │   ├── app/       # Next.js app router
    │   └── components/ # React components
    └── package.json   # Frontend dependencies
```

## Getting Started

### Backend Setup

```bash
cd backend
npm install
npm run dev
```

### Frontend Setup

```bash
cd frontend
bun install
bun run dev
```

## Features

- TypeScript for both frontend and backend
- Next.js App Router for frontend routing
- MongoDB with Mongoose for database
- JWT authentication
- TailwindCSS for styling
- Responsive design

## API Endpoints

- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login a user
- `GET /api/users/profile` - Get user profile (protected)

## Environment Variables

### Backend (.env)

- `PORT` - Server port (default: 5000)
- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET` - Secret for JWT token generation

### Frontend (.env.local)

- `NEXT_PUBLIC_API_URL` - Backend API URL
