<script lang="ts">
  export let title: string | undefined = undefined;
</script>

<div class="card">
  {#if title}
    <h3 class="text-xl font-semibold mb-3">{title}</h3>
  {/if}
  <div>
    <slot />
  </div>
</div> 