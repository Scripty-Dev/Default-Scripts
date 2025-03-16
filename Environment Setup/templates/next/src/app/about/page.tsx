const AboutPage = () => {
	return (
		<div className='max-w-4xl mx-auto'>
			<h1 className='text-3xl font-bold mb-6'>About Us</h1>

			<div className='card mb-8'>
				<h2 className='text-2xl font-semibold mb-4'>Our Mission</h2>
				<p className='mb-4'>
					Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui
					mauris. Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor
					neque eu tellus rhoncus ut eleifend nibh porttitor. Ut in nulla enim.
				</p>
				<p>
					Suspendisse in justo eu magna luctus suscipit. Sed lectus. Integer
					euismod lacus luctus magna. Quisque cursus, metus vitae pharetra
					auctor, sem massa mattis sem, at interdum magna augue eget diam.
				</p>
			</div>

			<div className='card mb-8'>
				<h2 className='text-2xl font-semibold mb-4'>Our Team</h2>
				<div className='grid grid-cols-1 md:grid-cols-3 gap-6'>
					<div className='text-center'>
						<div className='w-32 h-32 bg-gray-700 rounded-full mx-auto mb-4'></div>
						<h3 className='text-xl font-medium'>Jane Doe</h3>
						<p>CEO & Founder</p>
					</div>
					<div className='text-center'>
						<div className='w-32 h-32 bg-gray-700 rounded-full mx-auto mb-4'></div>
						<h3 className='text-xl font-medium'>John Smith</h3>
						<p>CTO</p>
					</div>
					<div className='text-center'>
						<div className='w-32 h-32 bg-gray-700 rounded-full mx-auto mb-4'></div>
						<h3 className='text-xl font-medium'>Emily Johnson</h3>
						<p>Lead Designer</p>
					</div>
				</div>
			</div>

			<div className='card'>
				<h2 className='text-2xl font-semibold mb-4'>Our Values</h2>
				<ul className='list-disc pl-5 space-y-2'>
					<li>Innovation and creativity in everything we do</li>
					<li>Customer satisfaction is our top priority</li>
					<li>Transparency and honesty in our operations</li>
					<li>Continuous learning and improvement</li>
					<li>Respect for our team members and clients</li>
				</ul>
			</div>
		</div>
	)
}

export default AboutPage
