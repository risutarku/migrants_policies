<!-- src/App.vue -->
<template>
  <!-- общий контейнер на весь экран -->
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <!-- сюда роутер вставит активную страницу -->
    <router-view />
  </div>
</template>

<script setup>
// здесь пока ничего не требуется
</script>

<style scoped>
/* при желании можно задать глобальные стили шрифта или фона */
</style>
