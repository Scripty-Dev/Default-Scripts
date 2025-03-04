import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'
import User from '../models/userModel'

// Extend Express Request type to include user
declare global {
	namespace Express {
		interface Request {
			user?: any
		}
	}
}

export const protect = async (
	req: Request,
	res: Response,
	next: NextFunction
) => {
	let token

	// Check if token exists in headers
	if (
		req.headers.authorization &&
		req.headers.authorization.startsWith('Bearer')
	) {
		try {
			// Get token from header
			token = req.headers.authorization.split(' ')[1]

			// Verify token
			const decoded = jwt.verify(token, process.env.JWT_SECRET as string) as {
				id: string
			}

			// Get user from the token
			req.user = await User.findById(decoded.id).select('-password')

			next()
		} catch (error) {
			console.error(error)
			res.status(401).json({ message: 'Not authorized, token failed' })
		}
	}

	if (!token) {
		res.status(401).json({ message: 'Not authorized, no token' })
	}
}
