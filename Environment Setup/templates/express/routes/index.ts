import express from 'express'
const router = express.Router()

// Health check endpoint
router.get('/health', (req, res) => {
	res.json({
		status: 'ok',
		message: 'Server is healthy',
		timestamp: new Date().toISOString(),
	})
})

// Example endpoint
router.get('/api/hello', (req, res) => {
	res.json({
		message: 'Hello from Express + TypeScript!',
		info: 'This API was initialized by Scripty',
	})
})

export default router
