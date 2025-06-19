<script setup>
defineProps({ selected: Boolean })
</script>

<template>
  <div
    class="rounded-xl p-6 border transition cursor-pointer"
    :class="selected
      ? 'border-brand bg-brand/5'
      : 'border-stroke hover:shadow-sm'"
  >
    <slot />
  </div>
</template>
