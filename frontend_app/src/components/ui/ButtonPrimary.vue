<script setup>
defineProps({ disabled: Boolean })
</script>

<template>
  <button
    :disabled="disabled"
    class="w-full py-4 text-xl font-semibold rounded-xl
           text-white bg-brand hover:bg-brand/90
           disabled:bg-surface disabled:text-brand/40
           transition"
  >
    <slot />
  </button>
</template>
