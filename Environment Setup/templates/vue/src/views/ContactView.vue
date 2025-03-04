<script setup lang="ts">
import { ref } from 'vue'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'

interface FormData {
	name: string
	email: string
	message: string
}

const formData = ref<FormData>({
	name: '',
	email: '',
	message: '',
})

const isSubmitting = ref(false)
const isSuccess = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
	isSubmitting.value = true
	errorMessage.value = ''

	try {
		// Simulate API call
		await new Promise((resolve) => setTimeout(resolve, 1000))

		// Reset form
		formData.value = {
			name: '',
			email: '',
			message: '',
		}

		isSuccess.value = true
		setTimeout(() => {
			isSuccess.value = false
		}, 5000)
	} catch (error) {
		errorMessage.value = 'An error occurred. Please try again.'
	} finally {
		isSubmitting.value = false
	}
}
</script>

<template>
	<div>
		<h1 class="text-3xl font-bold text-gray-900 mb-6">Contact Us</h1>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
			<Card>
				<form @submit.prevent="handleSubmit">
					<div class="mb-4">
						<label for="name" class="form-label">Name</label>
						<input
							id="name"
							v-model="formData.name"
							type="text"
							required
							class="form-input"
							placeholder="Your name"
						/>
					</div>

					<div class="mb-4">
						<label for="email" class="form-label">Email</label>
						<input
							id="email"
							v-model="formData.email"
							type="email"
							required
							class="form-input"
							placeholder="your.email@example.com"
						/>
					</div>

					<div class="mb-4">
						<label for="message" class="form-label">Message</label>
						<textarea
							id="message"
							v-model="formData.message"
							required
							rows="5"
							class="form-input"
							placeholder="Your message..."
						></textarea>
					</div>

					<div class="mt-6">
						<Button type="submit" variant="primary" :disabled="isSubmitting">
							{{ isSubmitting ? 'Sending...' : 'Send Message' }}
						</Button>
					</div>

					<div
						v-if="isSuccess"
						class="mt-4 p-3 bg-green-100 text-green-800 rounded"
					>
						Thank you for your message! We'll get back to you soon.
					</div>

					<div
						v-if="errorMessage"
						class="mt-4 p-3 bg-red-100 text-red-800 rounded"
					>
						{{ errorMessage }}
					</div>
				</form>
			</Card>

			<Card title="Get in Touch">
				<p class="mb-4">
					Have questions or feedback? We'd love to hear from you. Fill out the
					form and our team will get back to you as soon as possible.
				</p>

				<div class="space-y-4 mt-6">
					<div class="flex items-start">
						<div class="flex-shrink-0 text-primary-600">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
								/>
							</svg>
						</div>
						<div class="ml-3 text-gray-700">
							<p class="text-sm font-medium">Email</p>
							<p>contact@example.com</p>
						</div>
					</div>

					<div class="flex items-start">
						<div class="flex-shrink-0 text-primary-600">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
								/>
							</svg>
						</div>
						<div class="ml-3 text-gray-700">
							<p class="text-sm font-medium">Phone</p>
							<p>+1 (555) 123-4567</p>
						</div>
					</div>
				</div>
			</Card>
		</div>
	</div>
</template>
