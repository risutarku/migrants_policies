<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

const props = defineProps<{ label: string }>();
const emit = defineEmits<["click"]>();
</script>
<template>
  <button
    @click="emit('click')"
    class="block w-full rounded-2xl bg-primary py-4 px-6 text-white text-lg font-semibold shadow-lg shadow-primary/30 hover:bg-primary/90 active:shadow-none transition-all"
  >
    {{ label }}
  </button>
</template>
