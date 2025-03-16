import mongoose, { Document, Schema } from 'mongoose'

export interface IItem extends Document {
	name: string
	description: string
	price: number
	quantity: number
	category: string
	createdAt: Date
	updatedAt: Date
}

const ItemSchema = new Schema<IItem>(
	{
		name: {
			type: String,
			required: [true, 'Please add a name'],
			trim: true,
			maxlength: [50, 'Name cannot be more than 50 characters'],
		},
		description: {
			type: String,
			required: [true, 'Please add a description'],
			maxlength: [500, 'Description cannot be more than 500 characters'],
		},
		price: {
			type: Number,
			required: [true, 'Please add a price'],
			min: [0, 'Price must be a positive number'],
		},
		quantity: {
			type: Number,
			required: [true, 'Please add a quantity'],
			min: [0, 'Quantity must be a positive number'],
			default: 0,
		},
		category: {
			type: String,
			required: [true, 'Please add a category'],
			enum: ['electronics', 'clothing', 'food', 'books', 'other'],
			default: 'other',
		},
	},
	{
		timestamps: true,
	}
)

export default mongoose.model<IItem>('Item', ItemSchema)
