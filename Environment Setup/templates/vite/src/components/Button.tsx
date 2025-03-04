import { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
	variant?: 'primary' | 'secondary'
	size?: 'sm' | 'md' | 'lg'
}

const Button = ({
	children,
	variant = 'primary',
	size = 'md',
	className = '',
	...props
}: ButtonProps) => {
	const baseClasses = variant === 'primary' ? 'btn-primary' : 'btn-secondary'

	const sizeClasses = {
		sm: 'text-sm px-3 py-1',
		md: 'text-base px-4 py-2',
		lg: 'text-lg px-6 py-3',
	}

	return (
		<button
			className={`${baseClasses} ${sizeClasses[size]} ${className}`}
			{...props}
		>
			{children}
		</button>
	)
}

export default Button
