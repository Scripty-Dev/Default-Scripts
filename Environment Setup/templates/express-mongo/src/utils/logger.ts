enum LogLevel {
	INFO = 'INFO',
	WARN = 'WARN',
	ERROR = 'ERROR',
	DEBUG = 'DEBUG',
}

class Logger {
	private context: string

	constructor(context: string) {
		this.context = context
	}

	private formatMessage(level: LogLevel, message: string): string {
		const timestamp = new Date().toISOString()
		return `[${timestamp}] [${level}] [${this.context}]: ${message}`
	}

	info(message: string): void {
		console.log(this.formatMessage(LogLevel.INFO, message))
	}

	warn(message: string): void {
		console.warn(this.formatMessage(LogLevel.WARN, message))
	}

	error(message: string, error?: Error): void {
		console.error(this.formatMessage(LogLevel.ERROR, message))
		if (error && error.stack) {
			console.error(error.stack)
		}
	}

	debug(message: string): void {
		if (process.env.NODE_ENV === 'development') {
			console.debug(this.formatMessage(LogLevel.DEBUG, message))
		}
	}
}

export default Logger
