<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Button from '@/components/Button.vue'

const route = useRoute()
const appTitle = import.meta.env.VITE_APP_TITLE || '{{project_title}}'

const isActive = (path: string) => computed(() => route.path === path)
</script>

<template>
	<nav class="bg-white shadow-sm">
		<div class="container mx-auto px-4">
			<div class="flex justify-between h-16">
				<div class="flex items-center">
					<router-link to="/" class="flex-shrink-0 flex items-center">
						<span class="text-xl font-bold text-primary-600">{{
							appTitle
						}}</span>
					</router-link>
					<div class="hidden sm:ml-6 sm:flex sm:space-x-4">
						<router-link
							to="/"
							class="px-3 py-2 rounded-md text-sm font-medium"
							:class="
								isActive('/')
									? 'bg-primary-100 text-primary-900'
									: 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
							"
						>
							Home
						</router-link>
						<router-link
							to="/about"
							class="px-3 py-2 rounded-md text-sm font-medium"
							:class="
								isActive('/about')
									? 'bg-primary-100 text-primary-900'
									: 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
							"
						>
							About
						</router-link>
						<router-link
							to="/contact"
							class="px-3 py-2 rounded-md text-sm font-medium"
							:class="
								isActive('/contact')
									? 'bg-primary-100 text-primary-900'
									: 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
							"
						>
							Contact
						</router-link>
					</div>
				</div>
				<div class="flex items-center">
					<Button variant="primary"> Sign In </Button>
				</div>
			</div>
		</div>
	</nav>
</template>
