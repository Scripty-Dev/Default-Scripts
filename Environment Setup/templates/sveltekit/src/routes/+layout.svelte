<script>
  import '../app.postcss';
  import Navbar from '$lib/components/Navbar.svelte';
</script>

<Navbar />

<main class="container mx-auto px-4 py-8">
  <slot />
</main> 