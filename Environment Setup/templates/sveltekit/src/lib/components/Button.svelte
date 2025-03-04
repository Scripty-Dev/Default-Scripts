<script lang="ts">
  export let variant: 'primary' | 'secondary' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let type: 'button' | 'submit' | 'reset' = 'button';
  
  const baseClasses = variant === 'primary' ? 'btn-primary' : 'btn-secondary';
  
  const sizeClasses = {
    sm: 'text-sm px-3 py-1',
    md: 'text-base px-4 py-2',
    lg: 'text-lg px-6 py-3'
  };
</script>

<button 
  {type} 
  class="{baseClasses} {sizeClasses[size]}"
  on:click
>
  <slot />
</button> 