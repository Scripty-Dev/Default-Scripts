import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
  return {
    title: 'Welcome to SvelteKit',
    description: 'A modern web framework built on Svelte'
  };
}; 