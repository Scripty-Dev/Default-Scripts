import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Button from './components/Button'
import Card from './components/Card'

const Home = () => (
	<div className='space-y-8'>
		<section className='text-center py-12'>
			<h1 className='text-4xl font-bold mb-4'>Welcome to Vite + React</h1>
			<p className='text-xl text-gray-600 max-w-2xl mx-auto'>
				A modern React framework with fast development and optimized builds.
			</p>
			<div className='mt-8 flex justify-center gap-4'>
				<Button variant='primary'>Get Started</Button>
				<Button variant='secondary'>Learn More</Button>
			</div>
		</section>

		<section className='grid grid-cols-1 md:grid-cols-3 gap-6'>
			<Card title='Fast Development'>
				Instant server start and lightning-fast hot module replacement.
			</Card>
			<Card title='Optimized Build'>
				Pre-configured build optimizations with support for dynamic imports.
			</Card>
			<Card title='TypeScript Support'>
				First-class TypeScript support for better developer experience.
			</Card>
		</section>
	</div>
)

const App = () => {
	return (
		<>
			<Navbar />
			<main className='container mx-auto px-4 py-8'>
				<Routes>
					<Route path='/' element={<Home />} />
				</Routes>
			</main>
		</>
	)
}

export default App
