import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
	const count = ref(0)
	const doubleCount = computed(() => count.value * 2)

	const increment = () => {
		count.value++
	}

	const decrement = () => {
		count.value--
	}

	const reset = () => {
		count.value = 0
	}

	return {
		count,
		doubleCount,
		increment,
		decrement,
		reset,
	}
})
