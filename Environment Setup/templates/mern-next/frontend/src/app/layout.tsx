import type { Metadata } from 'next'
import { Hanken_Grotesk } from 'next/font/google'
import Navbar from '@/components/Navbar'
import './globals.css'

const hanken = Hanken_Grotesk({
	variable: '--font-hanken',
	subsets: ['latin'],
})

export const metadata: Metadata = {
	title: 'MERN Next.js App',
	description: 'A MERN stack application with Next.js frontend',
}

const RootLayout = ({ children }: { children: React.ReactNode }) => {
	return (
		<html lang='en'>
			<body className={`${hanken.variable} min-h-screen`}>
				<Navbar />
				<main className='container mx-auto px-4 py-8'>{children}</main>
				<h3 className='fixed right-4 bottom-4'>
					Initialized by{' '}
					<a
						target='_blank'
						href='https://scripty.me'
						className='text-purple-500 font-bold'
					>
						Scripty
					</a>
				</h3>
			</body>
		</html>
	)
}

export default RootLayout
