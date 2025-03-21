<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="text-center">
    <h1 class="text-4xl font-bold mb-8">
      Vue 3 + TypeScript + Tailwind project initialized by
      <span class="text-emerald-600">Scripty</span>
    </h1>

    <div class="bg-white rounded-xl shadow-lg p-6 mb-8 max-w-2xl mx-auto">
      <p class="text-gray-600 mb-4">
        Edit <code class="bg-gray-100 px-2 py-1 rounded">src/views/HomeView.vue</code> to test HMR
      </p>

      <div class="flex justify-center gap-4 items-center">
        <button
          type="button"
          class="px-4 py-2 font-semibold text-sm bg-emerald-500 text-white rounded-md shadow-sm hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
          @click="count++"
        >
          Count is: {{ count }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
      <!-- First Link -->
      <a href="https://vuejs.org/guide/introduction.html" target="_blank" class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-emerald-300 hover:bg-emerald-50">
        <h2 class="mb-3 text-2xl font-semibold">
          Documentation
          <span class="inline-block transition-transform group-hover:translate-x-1">-></span>
        </h2>
        <p class="text-sm opacity-70">Find in-depth information about Vue 3 features and API.</p>
      </a>

      <!-- Second Link -->
      <a href="https://pinia.vuejs.org/" target="_blank" class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-emerald-300 hover:bg-emerald-50">
        <h2 class="mb-3 text-2xl font-semibold">
          Pinia
          <span class="inline-block transition-transform group-hover:translate-x-1">-></span>
        </h2>
        <p class="text-sm opacity-70">Learn about Vue's official state management library.</p>
      </a>
    </div>
  </div>
</template>