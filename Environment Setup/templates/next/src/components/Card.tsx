'use client'

import { ReactNode } from 'react'

interface CardProps {
	title?: string
	children: ReactNode
	className?: string
}

const Card = ({ title, children, className = '' }: CardProps) => {
	return (
		<div className={`card ${className}`}>
			{title && <h3 className='text-xl font-semibold mb-3'>{title}</h3>}
			<div>{children}</div>
		</div>
	)
}

export default Card
