import Link from 'next/link'
import Card from '@/components/Card'
import Button from '@/components/Button'

export default function Home() {
	return (
		<div className='space-y-8'>
			<section className='text-center py-12'>
				<h1 className='text-4xl font-bold mb-4'>Welcome to Next.js</h1>
				<p className='text-xl text-gray-600 max-w-2xl mx-auto'>
					A modern React framework with server-side rendering, static site
					generation, and more.
				</p>
				<div className='mt-8 flex justify-center gap-4'>
					<Button variant='primary'>Get Started</Button>
					<Button variant='secondary'>Learn More</Button>
				</div>
			</section>

			<section className='grid grid-cols-1 md:grid-cols-3 gap-6'>
				<Card title='Server Components'>
					React Server Components allow you to write UI that can be rendered and
					optionally cached on the server.
				</Card>
				<Card title='Client Components'>
					Client Components enable you to add client-side interactivity to your
					application.
				</Card>
				<Card title='Streaming'>
					Streaming enables you to progressively render UI from the server,
					improving both the user and developer experience.
				</Card>
			</section>
		</div>
	)
}
