const ProjectsPage = () => {
	return (
		<div className='max-w-6xl mx-auto'>
			<h1 className='text-3xl font-bold mb-6'>Our Projects</h1>

			<div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
				{projects.map((project) => (
					<div
						key={project.id}
						className='card hover:shadow-lg transition-shadow'
					>
						<div className='h-48 bg-gray-700 mb-4 rounded-md'></div>
						<h2 className='text-xl font-semibold mb-2'>{project.title}</h2>
						<p className='mb-4'>{project.description}</p>
						<div className='flex flex-wrap gap-2 mb-4'>
							{project.technologies.map((tech) => (
								<span
									key={tech}
									className='px-2 py-1 bg-gray-700 rounded-md text-xs'
								>
									{tech}
								</span>
							))}
						</div>
						<button className='btn btn-primary w-full'>View Details</button>
					</div>
				))}
			</div>
		</div>
	)
}

const projects = [
	{
		id: 1,
		title: 'E-commerce Platform',
		description: 'A modern e-commerce platform for product management.',
		technologies: ['React', 'Next.js', 'Tailwind CSS', 'Stripe'],
	},
	{
		id: 2,
		title: 'Task Management App',
		description:
			'A collaborative task management application with real-time updates.',
		technologies: ['React', 'TypeScript', 'Tailwind CSS', 'Firebase'],
	},
	{
		id: 3,
		title: 'Portfolio Website',
		description:
			'A responsive portfolio website showcasing creative work and projects.',
		technologies: ['Next.js', 'Framer Motion', 'Tailwind CSS'],
	},
	{
		id: 4,
		title: 'Weather Dashboard',
		description:
			'A weather dashboard with location-based forecasts and interactive maps.',
		technologies: ['React', 'OpenWeather API', 'Chart.js'],
	},
	{
		id: 5,
		title: 'Recipe Sharing Platform',
		description:
			'A community-driven recipe sharing platform with search and filtering.',
		technologies: ['Next.js', 'TypeScript', 'Tailwind CSS'],
	},
	{
		id: 6,
		title: 'Fitness Tracker',
		description:
			'A fitness tracking application with workout plans and progress visualization.',
		technologies: ['React', 'TypeScript', 'Chart.js', 'Tailwind CSS'],
	},
]

export default ProjectsPage
