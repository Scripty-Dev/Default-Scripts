'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import axios from 'axios'

const Register = () => {
	const router = useRouter()
	const [formData, setFormData] = useState({
		name: '',
		email: '',
		password: '',
		confirmPassword: '',
	})
	const [error, setError] = useState('')
	const [loading, setLoading] = useState(false)

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target
		setFormData((prev) => ({ ...prev, [name]: value }))
	}

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		setError('')

		// Validate passwords match
		if (formData.password !== formData.confirmPassword) {
			setError('Passwords do not match')
			return
		}

		setLoading(true)

		try {
			const { name, email, password } = formData
			const response = await axios.post('/api/users/register', {
				name,
				email,
				password,
			})

			// Store token in localStorage
			localStorage.setItem('userToken', response.data.token)

			// Redirect to dashboard
			router.push('/dashboard')
		} catch (err) {
			setError(
				axios.isAxiosError(err) && err.response?.data?.message
					? err.response.data.message
					: 'Registration failed. Please try again.'
			)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className='flex justify-center items-center min-h-[70vh]'>
			<div className='card max-w-md w-full'>
				<h1 className='text-2xl font-bold mb-6 text-center'>Register</h1>

				{error && (
					<div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'>
						{error}
					</div>
				)}

				<form onSubmit={handleSubmit}>
					<div className='mb-4'>
						<label htmlFor='name' className='block text-gray-700 mb-2'>
							Name
						</label>
						<input
							type='text'
							id='name'
							name='name'
							className='input'
							value={formData.name}
							onChange={handleChange}
							required
						/>
					</div>

					<div className='mb-4'>
						<label htmlFor='email' className='block text-gray-700 mb-2'>
							Email
						</label>
						<input
							type='email'
							id='email'
							name='email'
							className='input'
							value={formData.email}
							onChange={handleChange}
							required
						/>
					</div>

					<div className='mb-4'>
						<label htmlFor='password' className='block text-gray-700 mb-2'>
							Password
						</label>
						<input
							type='password'
							id='password'
							name='password'
							className='input'
							value={formData.password}
							onChange={handleChange}
							required
							minLength={6}
						/>
					</div>

					<div className='mb-6'>
						<label
							htmlFor='confirmPassword'
							className='block text-gray-700 mb-2'
						>
							Confirm Password
						</label>
						<input
							type='password'
							id='confirmPassword'
							name='confirmPassword'
							className='input'
							value={formData.confirmPassword}
							onChange={handleChange}
							required
							minLength={6}
						/>
					</div>

					<button
						type='submit'
						className='btn btn-primary w-full'
						disabled={loading}
					>
						{loading ? 'Registering...' : 'Register'}
					</button>
				</form>

				<div className='mt-4 text-center'>
					<p>
						Already have an account?{' '}
						<Link href='/login' className='text-primary-600 hover:underline'>
							Login
						</Link>
					</p>
				</div>
			</div>
		</div>
	)
}

export default Register
