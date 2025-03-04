import Link from 'next/link'

const Home = () => {
	return (
		<div className='flex flex-col items-center justify-center min-h-[70vh]'>
			<div className='card max-w-2xl w-full text-center'>
				<h1 className='text-4xl font-bold mb-6'>Welcome to MERN Next.js App</h1>
				<p className='text-lg mb-8'>
					A full-stack application with MongoDB, Express, React, Node.js, and
					Next.js
				</p>

				<div className='flex flex-col sm:flex-row gap-4 justify-center'>
					<Link href='/login' className='btn btn-primary'>
						Login
					</Link>
					<Link href='/register' className='btn btn-secondary'>
						Register
					</Link>
				</div>

				<div className='mt-12 grid grid-cols-1 md:grid-cols-3 gap-6'>
					<div className='p-4 border rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>MongoDB</h2>
						<p>NoSQL database for storing application data</p>
					</div>
					<div className='p-4 border rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>Express & Node.js</h2>
						<p>Backend API server with TypeScript</p>
					</div>
					<div className='p-4 border rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>Next.js</h2>
						<p>React framework with server-side rendering</p>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Home
