'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const Navbar = () => {
	const pathname = usePathname()

	return (
		<nav className='bg-white shadow-md'>
			<div className='container mx-auto px-4'>
				<div className='flex justify-between items-center h-16'>
					<div className='flex items-center'>
						<Link href='/' className='text-xl font-bold text-primary-600'>
							MERN Next.js
						</Link>
					</div>

					<div className='flex space-x-4'>
						<NavLink href='/' current={pathname === '/'}>
							Home
						</NavLink>
						<NavLink href='/dashboard' current={pathname === '/dashboard'}>
							Dashboard
						</NavLink>
						<NavLink href='/login' current={pathname === '/login'}>
							Login
						</NavLink>
						<NavLink href='/register' current={pathname === '/register'}>
							Register
						</NavLink>
					</div>
				</div>
			</div>
		</nav>
	)
}

const NavLink = ({
	href,
	current,
	children,
}: {
	href: string
	current: boolean
	children: React.ReactNode
}) => {
	return (
		<Link
			href={href}
			className={`px-3 py-2 rounded-md text-sm font-medium ${
				current
					? 'bg-primary-100 text-primary-700'
					: 'text-gray-700 hover:bg-gray-100'
			}`}
		>
			{children}
		</Link>
	)
}

export default Navbar
