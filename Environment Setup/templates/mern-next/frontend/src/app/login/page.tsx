'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import axios from 'axios'

const Login = () => {
	const router = useRouter()
	const [formData, setFormData] = useState({
		email: '',
		password: '',
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
		setLoading(true)

		try {
			const response = await axios.post('/api/users/login', formData)

			// Store token in localStorage
			localStorage.setItem('userToken', response.data.token)

			// Redirect to dashboard
			router.push('/dashboard')
		} catch (err) {
			setError(
				axios.isAxiosError(err) && err.response?.data?.message
					? err.response.data.message
					: 'Login failed. Please try again.'
			)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className='flex justify-center items-center min-h-[70vh]'>
			<div className='card max-w-md w-full'>
				<h1 className='text-2xl font-bold mb-6 text-center'>Login</h1>

				{error && (
					<div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'>
						{error}
					</div>
				)}

				<form onSubmit={handleSubmit}>
					<div className='mb-4'>
						<label htmlFor='email' className='block mb-2'>
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

					<div className='mb-6'>
						<label htmlFor='password' className='block mb-2'>
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
						/>
					</div>

					<button
						type='submit'
						className='btn btn-primary w-full'
						disabled={loading}
					>
						{loading ? 'Logging in...' : 'Login'}
					</button>
				</form>

				<div className='mt-4 text-center'>
					<p>
						Don't have an account?{' '}
						<Link href='/register' className='text-gray-200 hover:underline'>
							Register
						</Link>
					</p>
				</div>
			</div>
		</div>
	)
}

export default Login
