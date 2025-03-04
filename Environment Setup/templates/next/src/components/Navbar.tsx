'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const NavLink = ({
	href,
	children,
}: {
	href: string
	children: React.ReactNode
}) => {
	const pathname = usePathname()
	const isActive = pathname === href

	return (
		<Link
			href={href}
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
						<Link href='/' className='flex-shrink-0 flex items-center'>
							<span className='text-xl font-bold text-primary-600'>
								Next.js App
							</span>
						</Link>
						<div className='hidden sm:ml-6 sm:flex sm:space-x-2'>
							<NavLink href='/'>Home</NavLink>
							<NavLink href='/about'>About</NavLink>
							<NavLink href='/contact'>Contact</NavLink>
						</div>
					</div>
					<div className='flex items-center'>
						<button className='btn-secondary'>Sign In</button>
					</div>
				</div>
			</div>
		</nav>
	)
}

export default Navbar
