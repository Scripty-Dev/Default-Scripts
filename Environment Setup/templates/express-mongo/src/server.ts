import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import { config } from 'dotenv'
import connectDB from './config/db'
import { errorHandler } from './middleware/errorMiddleware'

// Import routes
import itemRoutes from './routes/itemRoutes'

// Load environment variables
config()

// Initialize express app
const app = express()
const PORT = process.env.PORT || 5000

// Connect to MongoDB
connectDB()

// Middleware
app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(cors())
app.use(helmet())
app.use(morgan('dev'))

// Routes
app.use('/api/items', itemRoutes)

// Health check route
app.get('/health', (req, res) => {
	res.status(200).json({ status: 'ok', message: 'Server is running' })
})

// Error handler middleware (should be last)
app.use(errorHandler)

// Start server
app.listen(PORT, () => {
	console.log(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`)
})

export default app
