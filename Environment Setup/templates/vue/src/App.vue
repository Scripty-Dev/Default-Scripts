<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
	<header>
		<Navbar />
	</header>

	<main class="container mx-auto px-4 py-8">
		<RouterView />
	</main>

	<footer class="bg-gray-100 py-6 mt-12">
		<div class="container mx-auto px-4 text-center text-gray-600">
			<p>
				&copy; {{ new Date().getFullYear() }} {{ project_title }}. All rights
				reserved.
			</p>
		</div>
	</footer>
</template>
