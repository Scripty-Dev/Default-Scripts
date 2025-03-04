import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import mongoose from 'mongoose'
import userRoutes from './routes/userRoutes'

// Load environment variables
dotenv.config()

// Create Express app
const app = express()
const PORT = process.env.PORT || 5000

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.use('/api/users', userRoutes)

// Health check route
app.get('/api/health', (req, res) => {
	res.json({ status: 'ok', message: 'API is running' })
})

// Connect to MongoDB
const connectDB = async () => {
	try {
		const conn = await mongoose.connect(process.env.MONGODB_URI as string)
		console.log(`MongoDB Connected: ${conn.connection.host}`)
	} catch (error) {
		console.error(
			`Error: ${error instanceof Error ? error.message : String(error)}`
		)
		process.exit(1)
	}
}

// Start server
connectDB().then(() => {
	app.listen(PORT, () => {
		console.log(`Server running on port ${PORT}`)
	})
})
