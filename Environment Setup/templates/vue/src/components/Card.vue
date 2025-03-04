<script setup lang="ts">
interface Props {
	title?: string
	className?: string
}

defineProps<Props>()
</script>

<template>
	<div class="card" :class="className">
		<h3 v-if="title" class="text-xl font-semibold mb-3">{{ title }}</h3>
		<div>
			<slot></slot>
		</div>
	</div>
</template>
