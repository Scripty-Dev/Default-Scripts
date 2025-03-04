import { useLocation, Link } from 'react-router-dom'
import Button from './Button'

const NavLink = ({
	to,
	children,
}: {
	to: string
	children: React.ReactNode
}) => {
	const { pathname } = useLocation()
	const isActive = pathname === to

	return (
		<Link
			to={to}
			className={`px-3 py-2 rounded-md text-sm font-medium ${
				isActive
					? 'bg-primary-100 text-primary-900'
					: 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
			}`}
		>
			{children}
		</Link>
	)
}

const Navbar = () => {
	return (
		<nav className='bg-white shadow-sm'>
			<div className='container mx-auto px-4'>
				<div className='flex justify-between h-16'>
					<div className='flex items-center'>
						<Link to='/' className='flex-shrink-0 flex items-center'>
							<span className='text-xl font-bold text-primary-600'>
								Vite App
							</span>
						</Link>
						<div className='hidden sm:ml-6 sm:flex sm:space-x-2'>
							<NavLink to='/'>Home</NavLink>
							<NavLink to='/about'>About</NavLink>
							<NavLink to='/contact'>Contact</NavLink>
						</div>
					</div>
					<div className='flex items-center'>
						<Button variant='secondary'>Sign In</Button>
					</div>
				</div>
			</div>
		</nav>
	)
}

export default Navbar
