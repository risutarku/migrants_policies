<!-- Welcome.vue -->
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { SUPPORTED as languages, setLocale } from '@/i18n'
import { useRouter } from 'vue-router'
import { useFlowStore } from '@/store'

const router = useRouter()
const { locale, t } = useI18n()
const current = computed(() => locale.value)
const changing = ref(false)
const store = useFlowStore() // импортируем store для доступа к lang

async function changeLang(code: string) {
  if (code === current.value || changing.value) return
  changing.value = true
  await setLocale(code)
  locale.value = code
  store.lang = code // подгружаем JSON и меняем locale
  changing.value = false
}

function handleClick() {
  router.push('/choose_policy') // переход на страницу выбора полиса
  // Здесь можно добавить логику для сохранения выбранного языка, если нужно
  // Например, сохранить в локальное хранилище или Vuex store
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-6 max-w-2xl flex-1"
    >
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl whitespace-pre-line">
        {{ t('landing.title') }}
      </h1>

      <p class="text-base sm:text-lg md:text-xl leading-relaxed">
        {{ t('landing.subtitle') }}
      </p>

      <!-- Language selector (reactive) -->
      <div
        class="w-64 max-h-40 overflow-y-auto border border-gray-300 rounded-xl divide-y divide-gray-200 shadow-sm bg-white"
      >
        <button
          v-for="lang in languages"
          :key="lang.code"
          @click="changeLang(lang.code)"
          class="w-full flex items-center gap-3 px-4 py-2 text-sm text-left transition-colors disabled:opacity-50 disabled:pointer-events-none"
          :class="lang.code === current ? 'bg-blue-50 font-medium text-blue-700' : 'hover:bg-gray-50'"
          :disabled="changing && lang.code !== current"
        >
          <img
            :src="`/flags/${lang.code}.svg`"
            :alt="lang.label"
            class="w-5 h-5 rounded-full object-cover shrink-0"
            @error="($event.target as HTMLImageElement).style.display='none'"
          />
          <span>{{ lang.label }}</span>
        </button>
      </div>
    </main>

    <!-- Logo -->
    <img
      src="/logo_ing.svg"
      alt="Ingosstrakh logo"
      class="w-60 h-auto my-6 select-none pointer-events-none"
    />

    <!-- CTA button -->
    <button
      @click="handleClick"
      class="w-full max-w-xs rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all"
    >
      {{ t('landing.cta') }}
    </button>
  </div>
</template>
