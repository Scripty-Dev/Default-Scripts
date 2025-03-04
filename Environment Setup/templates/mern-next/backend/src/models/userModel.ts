import mongoose from 'mongoose'

export interface IUser {
	name: string
	email: string
	password: string
	createdAt: Date
	updatedAt: Date
}

const userSchema = new mongoose.Schema<IUser>(
	{
		name: {
			type: String,
			required: [true, 'Please add a name'],
		},
		email: {
			type: String,
			required: [true, 'Please add an email'],
			unique: true,
			match: [
				/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
				'Please add a valid email',
			],
		},
		password: {
			type: String,
			required: [true, 'Please add a password'],
			minlength: 6,
		},
	},
	{
		timestamps: true,
	}
)

const User = mongoose.model<IUser>('User', userSchema)

export default User
