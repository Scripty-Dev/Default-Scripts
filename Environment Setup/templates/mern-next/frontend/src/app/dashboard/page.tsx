'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

interface User {
	_id: string
	name: string
	email: string
}

const Dashboard = () => {
	const router = useRouter()
	const [user, setUser] = useState<User | null>(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')

	useEffect(() => {
		const fetchUserProfile = async () => {
			const token = localStorage.getItem('userToken')

			if (!token) {
				router.push('/login')
				return
			}

			try {
				const response = await axios.get('/api/users/profile', {
					headers: {
						Authorization: `Bearer ${token}`,
					},
				})

				setUser(response.data)
			} catch (err) {
				setError('Failed to load user profile')
				// If unauthorized, redirect to login
				if (axios.isAxiosError(err) && err.response?.status === 401) {
					localStorage.removeItem('userToken')
					router.push('/login')
				}
			} finally {
				setLoading(false)
			}
		}

		fetchUserProfile()
	}, [router])

	const handleLogout = () => {
		localStorage.removeItem('userToken')
		router.push('/login')
	}

	if (loading) {
		return (
			<div className='flex justify-center items-center min-h-[70vh]'>
				<div className='text-xl'>Loading...</div>
			</div>
		)
	}

	return (
		<div className='flex flex-col items-center justify-center min-h-[70vh]'>
			<div className='card max-w-2xl w-full'>
				<div className='flex justify-between items-center mb-6'>
					<h1 className='text-2xl font-bold'>Dashboard</h1>
					<button onClick={handleLogout} className='btn btn-secondary'>
						Logout
					</button>
				</div>

				{error ? (
					<div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'>
						{error}
					</div>
				) : user ? (
					<div>
						<div className='mb-4 p-4 bg-gray-50 rounded-lg'>
							<h2 className='text-lg font-semibold mb-2'>User Profile</h2>
							<p>
								<span className='font-medium'>Name:</span> {user.name}
							</p>
							<p>
								<span className='font-medium'>Email:</span> {user.email}
							</p>
							<p>
								<span className='font-medium'>ID:</span> {user._id}
							</p>
						</div>

						<div className='mt-6'>
							<h2 className='text-lg font-semibold mb-4'>What's Next?</h2>
							<div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
								<div className='p-4 border rounded-lg'>
									<h3 className='font-medium mb-2'>Build Your App</h3>
									<p className='text-sm text-gray-600'>
										Start adding more features to your MERN stack application.
									</p>
								</div>
								<div className='p-4 border rounded-lg'>
									<h3 className='font-medium mb-2'>Explore the API</h3>
									<p className='text-sm text-gray-600'>
										Check out the backend API endpoints and integrate them.
									</p>
								</div>
							</div>
						</div>
					</div>
				) : (
					<p>No user data available</p>
				)}
			</div>
		</div>
	)
}

export default Dashboard
