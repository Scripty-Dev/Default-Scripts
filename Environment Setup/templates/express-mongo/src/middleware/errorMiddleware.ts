import { Request, Response, NextFunction } from 'express'

interface ErrorResponse {
	message: string
	stack?: string
}

export class ApiError extends Error {
	statusCode: number

	constructor(message: string, statusCode: number) {
		super(message)
		this.statusCode = statusCode
	}
}

export const errorHandler = (
	err: Error | ApiError,
	req: Request,
	res: Response,
	next: NextFunction
): void => {
	// Default to 500 server error
	const statusCode = 'statusCode' in err ? err.statusCode : 500

	const errorResponse: ErrorResponse = {
		message: err.message || 'Server Error',
	}

	// Add stack trace in development mode
	if (process.env.NODE_ENV === 'development') {
		errorResponse.stack = err.stack
	}

	res.status(statusCode).json(errorResponse)
}
