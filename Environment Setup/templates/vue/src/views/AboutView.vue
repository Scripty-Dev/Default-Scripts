<script setup lang="ts">
import Card from '@/components/Card.vue'

const appTitle = import.meta.env.VITE_APP_TITLE || '{{project_title}}'
</script>

<template>
	<div>
		<h1 class="text-3xl font-bold text-gray-900 mb-6">About {{ appTitle }}</h1>

		<div class="prose prose-lg max-w-none mb-8">
			<p>
				This is a modern Vue.js application built with the latest technologies
				and best practices. It serves as a starting point for your own projects,
				providing a solid foundation with all the essential features already set
				up.
			</p>
		</div>

		<Card title="Technology Stack" className="mb-8">
			<ul class="list-disc pl-5 space-y-2">
				<li>
					<strong>Vue 3:</strong> The progressive JavaScript framework for
					building user interfaces.
				</li>
				<li>
					<strong>TypeScript:</strong> Adds static typing to JavaScript to
					improve developer experience.
				</li>
				<li>
					<strong>Vite:</strong> Next generation frontend tooling for faster
					development.
				</li>
				<li>
					<strong>Tailwind CSS:</strong> A utility-first CSS framework for rapid
					UI development.
				</li>
				<li>
					<strong>Pinia:</strong> Intuitive, type safe and flexible Store for
					Vue.
				</li>
				<li><strong>Vue Router:</strong> The official router for Vue.js.</li>
			</ul>
		</Card>

		<Card title="Project Structure">
			<p class="mb-4">
				The project follows a standard Vue.js application structure:
			</p>
			<ul
				class="list-disc pl-5 space-y-1 text-sm font-mono bg-gray-50 p-4 rounded"
			>
				<li>src/</li>
				<li>├── assets/</li>
				<li>├── components/</li>
				<li>├── router/</li>
				<li>├── stores/</li>
				<li>├── views/</li>
				<li>├── App.vue</li>
				<li>└── main.ts</li>
			</ul>
		</Card>
	</div>
</template>
