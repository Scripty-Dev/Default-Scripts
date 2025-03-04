import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import { errorHandler } from './middleware/errorHandler'
import indexRouter from './routes'

// Load environment variables
dotenv.config()

const app = express()
const port = process.env.PORT || 3000

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.use('/', indexRouter)

// Error handling
app.use(errorHandler)

app.listen(port, () => {
	console.log(`[server]: Server is running at http://localhost:${port}`)
	console.log(`Environment: ${process.env.NODE_ENV}`)
})
