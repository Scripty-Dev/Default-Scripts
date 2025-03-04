<script>
  import Button from '$lib/components/Button.svelte';
  import Card from '$lib/components/Card.svelte';
</script>

<div class="space-y-8">
  <section class="text-center py-12">
    <h1 class="text-4xl font-bold mb-4">Welcome to SvelteKit</h1>
    <p class="text-xl text-gray-600 max-w-2xl mx-auto">
      A modern web framework built on Svelte, with server-side rendering, routing, and more.
    </p>
    <div class="mt-8 flex justify-center gap-4">
      <Button variant="primary">Get Started</Button>
      <Button variant="secondary">Learn More</Button>
    </div>
  </section>

  <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <Card title="Server-side Rendering">
      SvelteKit renders pages on the server, providing better performance and SEO benefits.
    </Card>
    <Card title="File-based Routing">
      Create routes by adding files to your project's routes directory. Simple and intuitive.
    </Card>
    <Card title="Progressive Enhancement">
      Works with JavaScript disabled, then enhances the experience when JavaScript is available.
    </Card>
  </section>
</div> 