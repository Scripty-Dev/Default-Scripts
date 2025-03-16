import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'
import { ApiError } from './errorMiddleware'

// Extend Express Request interface to include user
declare global {
	namespace Express {
		interface Request {
			user?: any
		}
	}
}

interface JwtPayload {
	id: string
}

export const protect = async (
	req: Request,
	res: Response,
	next: NextFunction
): Promise<void> => {
	let token

	// Check if auth header exists and starts with Bearer
	if (
		req.headers.authorization &&
		req.headers.authorization.startsWith('Bearer')
	) {
		try {
			// Get token from header
			token = req.headers.authorization.split(' ')[1]

			// Verify token
			const decoded = jwt.verify(
				token,
				process.env.JWT_SECRET as string
			) as JwtPayload

			// Add user to request
			req.user = { id: decoded.id }

			next()
		} catch (error) {
			next(new ApiError('Not authorized, token failed', 401))
		}
	} else {
		next(new ApiError('Not authorized, no token', 401))
	}
}
