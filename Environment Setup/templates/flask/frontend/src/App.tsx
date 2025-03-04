import { useState, useEffect } from 'react'
import axios from 'axios'

const App = () => {
	const [message, setMessage] = useState<string>('')
	const [loading, setLoading] = useState<boolean>(true)

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await axios.get('/api/test')
				setMessage(response.data.message)
			} catch (error) {
				setMessage('Error connecting to API')
				console.error(error)
			} finally {
				setLoading(false)
			}
		}

		fetchData()
	}, [])

	return (
		<div className='min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4'>
			<div className='bg-white p-8 rounded-lg shadow-md max-w-md w-full'>
				<h1 className='text-2xl font-bold text-center mb-6'>
					Flask + React App
				</h1>

				<div className='bg-gray-50 p-4 rounded border'>
					{loading ? (
						<p className='text-center text-gray-500'>Loading...</p>
					) : (
						<p className='text-center'>{message}</p>
					)}
				</div>

				<div className='mt-6 text-center text-sm text-gray-500'>
					<p>
						Edit <code className='bg-gray-100 p-1 rounded'>src/App.tsx</code> to
						get started
					</p>
				</div>
			</div>
		</div>
	)
}

export default App
