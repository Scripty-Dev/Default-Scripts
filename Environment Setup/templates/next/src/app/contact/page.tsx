'use client'

import { useState } from 'react'

const ContactPage = () => {
	const [formData, setFormData] = useState({
		name: '',
		email: '',
		message: '',
	})
	const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')

	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		const { name, value } = e.target
		setFormData((prev) => ({ ...prev, [name]: value }))
	}

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault()
		setStatus('success')

		// In a real app, you would send the form data to your backend
		console.log('Form submitted:', formData)

		// Reset form after 3 seconds
		setTimeout(() => {
			setFormData({ name: '', email: '', message: '' })
			setStatus('idle')
		}, 3000)
	}

	return (
		<div className='max-w-2xl mx-auto'>
			<h1 className='text-3xl font-bold mb-6'>Contact Us</h1>

			<div className='card mb-8'>
				<div className='grid grid-cols-1 md:grid-cols-2 gap-6 mb-6'>
					<div>
						<h2 className='text-xl font-semibold mb-2'>Get in Touch</h2>
						<p className='mb-4'>
							Have a question or want to work together? Fill out the form and
							we'll get back to you as soon as possible.
						</p>
						<div className='space-y-2'>
							<p className='flex items-center'>
								<span className='mr-2'>📍</span> 123 Demo Street, City, Country
							</p>
							<p className='flex items-center'>
								<span className='mr-2'>📧</span> contact@example.com
							</p>
							<p className='flex items-center'>
								<span className='mr-2'>📱</span> +1 (555) 123-4567
							</p>
						</div>
					</div>
					<div>
						<h2 className='text-xl font-semibold mb-2'>Office Hours</h2>
						<ul className='space-y-1'>
							<li>Monday - Friday: 9am - 5pm</li>
							<li>Saturday: 10am - 2pm</li>
							<li>Sunday: Closed</li>
						</ul>
					</div>
				</div>
			</div>

			<div className='card'>
				<h2 className='text-xl font-semibold mb-4'>Send a Message</h2>

				{status === 'success' && (
					<div className='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4'>
						Thank you for your message! We'll get back to you soon.
					</div>
				)}

				{status === 'error' && (
					<div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'>
						There was an error sending your message. Please try again.
					</div>
				)}

				<form onSubmit={handleSubmit}>
					<div className='mb-4'>
						<label htmlFor='name' className='block mb-2'>
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
						<label htmlFor='message' className='block mb-2'>
							Message
						</label>
						<textarea
							id='message'
							name='message'
							rows={5}
							className='input'
							value={formData.message}
							onChange={handleChange}
							required
						></textarea>
					</div>

					<button type='submit' className='btn btn-primary w-full'>
						Send Message
					</button>
				</form>
			</div>
		</div>
	)
}

export default ContactPage
