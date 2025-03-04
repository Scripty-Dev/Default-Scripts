<script setup lang="ts">
import Card from '@/components/Card.vue'

const appTitle = import.meta.env.VITE_APP_TITLE || '{{project_title}}'
</script>

<template>
	<div>
		<h1 class="text-3xl font-bold text-gray-900 mb-6">
			Welcome to {{ appTitle }}
		</h1>

		<p class="text-lg text-gray-700 mb-8">
			A modern Vue 3 application with TypeScript, Tailwind CSS, and Pinia for
			state management.
		</p>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
			<Card title="Vue 3 + TypeScript">
				<p>
					Built with Vue 3's Composition API and TypeScript for type safety and
					better developer experience.
				</p>
			</Card>

			<Card title="Tailwind CSS">
				<p>
					Styled with Tailwind CSS for rapid UI development with utility-first
					approach.
				</p>
			</Card>

			<Card title="Pinia Store">
				<p>
					State management with Pinia, the official Vue store that's intuitive
					and type-safe.
				</p>
			</Card>
		</div>

		<div class="bg-primary-50 p-6 rounded-lg border border-primary-100">
			<h2 class="text-xl font-semibold text-primary-900 mb-3">
				Getting Started
			</h2>
			<p class="text-primary-800 mb-4">
				Edit
				<code class="bg-primary-100 px-1 py-0.5 rounded"
					>src/views/HomeView.vue</code
				>
				to customize this page.
			</p>
			<p class="text-primary-800">
				Check out the
				<code class="bg-primary-100 px-1 py-0.5 rounded">README.md</code> file
				for more information on the project structure.
			</p>
		</div>
	</div>
</template>
