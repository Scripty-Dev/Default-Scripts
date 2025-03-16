import Link from 'next/link'

const Home = () => {
	return (
		<div className='flex flex-col items-center justify-center min-h-[70vh]'>
			<div className='card max-w-2xl w-full text-center'>
				<h1 className='text-4xl font-bold mb-6'>Welcome to Next.js Demo</h1>
				<p className='text-lg mb-8'>
					A modern web application built with Next.js and React
				</p>

				<div className='flex flex-col sm:flex-row gap-4 justify-center'>
					<Link href='/projects' className='btn btn-primary'>
						View Projects
					</Link>
					<Link href='/contact' className='btn btn-secondary'>
						Contact Us
					</Link>
				</div>

				<div className='mt-12 grid grid-cols-1 md:grid-cols-3 gap-6'>
					<div className='p-4 border border-gray-700 rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>Modern UI</h2>
						<p>Beautiful and responsive user interface</p>
					</div>
					<div className='p-4 border border-gray-700 rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>Fast Performance</h2>
						<p>Optimized for speed and user experience</p>
					</div>
					<div className='p-4 border border-gray-700 rounded-lg'>
						<h2 className='text-xl font-semibold mb-2'>Easy to Use</h2>
						<p>Intuitive design and navigation</p>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Home
