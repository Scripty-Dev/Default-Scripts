import { Request, Response } from 'express'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import User from '../models/userModel'

// @desc    Register a new user
// @route   POST /api/users/register
// @access  Public
export const register = async (req: Request, res: Response) => {
	try {
		const { name, email, password } = req.body

		// Check if user already exists
		const userExists = await User.findOne({ email })
		if (userExists) {
			return res.status(400).json({ message: 'User already exists' })
		}

		// Hash password
		const salt = await bcrypt.genSalt(10)
		const hashedPassword = await bcrypt.hash(password, salt)

		// Create user
		const user = await User.create({
			name,
			email,
			password: hashedPassword,
		})

		if (user) {
			res.status(201).json({
				_id: user._id,
				name: user.name,
				email: user.email,
				token: generateToken(user._id.toString()),
			})
		} else {
			res.status(400).json({ message: 'Invalid user data' })
		}
	} catch (error) {
		res.status(500).json({
			message: 'Server error',
			error: error instanceof Error ? error.message : String(error),
		})
	}
}

// @desc    Authenticate user & get token
// @route   POST /api/users/login
// @access  Public
export const login = async (req: Request, res: Response) => {
	try {
		const { email, password } = req.body

		// Check for user email
		const user = await User.findOne({ email })

		if (user && (await bcrypt.compare(password, user.password))) {
			res.json({
				_id: user._id,
				name: user.name,
				email: user.email,
				token: generateToken(user._id.toString()),
			})
		} else {
			res.status(401).json({ message: 'Invalid email or password' })
		}
	} catch (error) {
		res.status(500).json({
			message: 'Server error',
			error: error instanceof Error ? error.message : String(error),
		})
	}
}

// @desc    Get user profile
// @route   GET /api/users/profile
// @access  Private
export const getProfile = async (req: Request, res: Response) => {
	try {
		// req.user is set by the auth middleware
		const user = await User.findById(req.user?._id).select('-password')

		if (user) {
			res.json(user)
		} else {
			res.status(404).json({ message: 'User not found' })
		}
	} catch (error) {
		res.status(500).json({
			message: 'Server error',
			error: error instanceof Error ? error.message : String(error),
		})
	}
}

// Generate JWT
const generateToken = (id: string) => {
	return jwt.sign({ id }, process.env.JWT_SECRET as string, {
		expiresIn: '30d',
	})
}
