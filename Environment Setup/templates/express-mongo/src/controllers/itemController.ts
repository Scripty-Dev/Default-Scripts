import { Request, Response } from 'express'
import Item, { IItem } from '../models/Item'
import { ApiError } from '../middleware/errorMiddleware'

// @desc    Get all items
// @route   GET /api/items
// @access  Public
export const getItems = async (req: Request, res: Response): Promise<void> => {
	try {
		const items = await Item.find().sort({ createdAt: -1 })
		res.status(200).json({ success: true, count: items.length, data: items })
	} catch (error) {
		res.status(500).json({ success: false, error: 'Server Error' })
	}
}

// @desc    Get single item
// @route   GET /api/items/:id
// @access  Public
export const getItem = async (req: Request, res: Response): Promise<void> => {
	try {
		const item = await Item.findById(req.params.id)

		if (!item) {
			throw new ApiError(`Item not found with id of ${req.params.id}`, 404)
		}

		res.status(200).json({ success: true, data: item })
	} catch (error) {
		if (error instanceof ApiError) {
			res
				.status(error.statusCode)
				.json({ success: false, error: error.message })
		} else {
			res.status(500).json({ success: false, error: 'Server Error' })
		}
	}
}

// @desc    Create new item
// @route   POST /api/items
// @access  Public
export const createItem = async (
	req: Request,
	res: Response
): Promise<void> => {
	try {
		const item = await Item.create(req.body)
		res.status(201).json({ success: true, data: item })
	} catch (error) {
		if (error instanceof Error) {
			res.status(400).json({ success: false, error: error.message })
		} else {
			res.status(500).json({ success: false, error: 'Server Error' })
		}
	}
}

// @desc    Update item
// @route   PUT /api/items/:id
// @access  Public
export const updateItem = async (
	req: Request,
	res: Response
): Promise<void> => {
	try {
		const item = await Item.findByIdAndUpdate(req.params.id, req.body, {
			new: true,
			runValidators: true,
		})

		if (!item) {
			throw new ApiError(`Item not found with id of ${req.params.id}`, 404)
		}

		res.status(200).json({ success: true, data: item })
	} catch (error) {
		if (error instanceof ApiError) {
			res
				.status(error.statusCode)
				.json({ success: false, error: error.message })
		} else if (error instanceof Error) {
			res.status(400).json({ success: false, error: error.message })
		} else {
			res.status(500).json({ success: false, error: 'Server Error' })
		}
	}
}

// @desc    Delete item
// @route   DELETE /api/items/:id
// @access  Public
export const deleteItem = async (
	req: Request,
	res: Response
): Promise<void> => {
	try {
		const item = await Item.findById(req.params.id)

		if (!item) {
			throw new ApiError(`Item not found with id of ${req.params.id}`, 404)
		}

		await item.deleteOne()

		res.status(200).json({ success: true, data: {} })
	} catch (error) {
		if (error instanceof ApiError) {
			res
				.status(error.statusCode)
				.json({ success: false, error: error.message })
		} else {
			res.status(500).json({ success: false, error: 'Server Error' })
		}
	}
}
