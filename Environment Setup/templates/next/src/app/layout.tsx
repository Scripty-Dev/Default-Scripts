import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/Navbar'

export const metadata: Metadata = {
	title: 'Next.js App',
	description: 'A modern Next.js application with TypeScript and Tailwind CSS',
}

export default function RootLayout({
	children,
}: {
	children: React.ReactNode
}) {
	return (
		<html lang='en'>
			<body>
				<Navbar />
				<main className='container mx-auto px-4 py-8'>{children}</main>
			</body>
		</html>
	)
}
