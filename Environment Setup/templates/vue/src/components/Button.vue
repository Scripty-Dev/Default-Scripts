<script setup lang="ts">
interface Props {
	variant?: 'primary' | 'secondary'
	type?: 'button' | 'submit' | 'reset'
	disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
	variant: 'primary',
	type: 'button',
	disabled: false,
})
</script>

<template>
	<button
		:type="type"
		:disabled="disabled"
		class="btn"
		:class="{
			'btn-primary': variant === 'primary',
			'btn-secondary': variant === 'secondary',
			'opacity-50 cursor-not-allowed': disabled,
		}"
	>
		<slot></slot>
	</button>
</template>
