<script lang="ts">
  import { page } from '$app/stores';
  import Button from './Button.svelte';
  
  const links = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/contact', label: 'Contact' }
  ];
</script>

<nav class="bg-white shadow-sm">
  <div class="container mx-auto px-4">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <a href="/" class="flex-shrink-0 flex items-center">
          <span class="text-xl font-bold text-primary-600">SvelteKit App</span>
        </a>
        <div class="hidden sm:ml-6 sm:flex sm:space-x-2">
          {#each links as link}
            <a 
              href={link.href} 
              class="px-3 py-2 rounded-md text-sm font-medium {$page.url.pathname === link.href 
                ? 'bg-primary-100 text-primary-900' 
                : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'}"
            >
              {link.label}
            </a>
          {/each}
        </div>
      </div>
      <div class="flex items-center">
        <Button variant="secondary">Sign In</Button>
      </div>
    </div>
  </div>
</nav> 