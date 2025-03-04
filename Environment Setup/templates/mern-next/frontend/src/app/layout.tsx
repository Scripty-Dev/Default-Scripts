import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/Navbar'

export const metadata: Metadata = {
	title: 'MERN Next.js App',
	description: 'A MERN stack application with Next.js frontend',
}

const RootLayout = ({ children }: { children: React.ReactNode }) => {
	return (
		<html lang='en'>
			<body>
				<Navbar />
				<main className='container mx-auto px-4 py-8'>{children}</main>
			</body>
		</html>
	)
}

export default RootLayout
