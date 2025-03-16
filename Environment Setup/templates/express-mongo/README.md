A modern Express.js API with MongoDB integration using TypeScript.

## Project Structure

```
├── src/
│   ├── config/         # Configuration files
│   │   └── db.ts       # Database connection
│   ├── controllers/    # Route controllers
│   │   └── itemController.ts
│   ├── middleware/     # Custom middleware
│   │   ├── authMiddleware.ts
│   │   └── errorMiddleware.ts
│   ├── models/         # Mongoose models
│   │   └── Item.ts
│   ├── routes/         # API routes
│   │   └── itemRoutes.ts
│   ├── utils/          # Utility functions
│   │   └── logger.ts
│   └── server.ts       # Entry point
├── .env        # Example environment variables
├── package.json        # Project dependencies
├── tsconfig.json       # TypeScript configuration
└── README.md           # Project documentation
```

## Getting Started

```bash
bun dev
```

## Features

- RESTful API structure with Express.js
- MongoDB integration with Mongoose
- TypeScript for type safety
- JWT authentication
- Error handling middleware
- Environment configuration
- Logging utility

## API Endpoints

- `GET /api/items` - Get all items
- `GET /api/items/:id` - Get a single item
- `POST /api/items` - Create a new item
- `PUT /api/items/:id` - Update an item
- `DELETE /api/items/:id` - Delete an item

## Environment Variables

- `PORT` - Server port (default: 5000)
- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET` - Secret for JWT token generation

This template was initialized by [Scripty](https://scripty.me).
