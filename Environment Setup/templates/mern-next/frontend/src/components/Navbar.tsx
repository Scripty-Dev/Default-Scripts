'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const Navbar = () => {
	const pathname = usePathname()

	return (
		<nav className='bg-bg shadow-md'>
			<div className='container mx-auto px-4'>
				<div className='flex justify-between items-center h-16'>
					<div className='flex items-center'>
						<Link href='/' className='text-xl font-bold'>
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
			className={`px-3 py-2 rounded-md text-sm font-medium duration-300 ${
				current ? '' : 'text-gray-400 hover:text-gray-100'
			}`}
		>
			{children}
		</Link>
	)
}

export default Navbar
