<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useFlowStore } from '@/store'
import { computed } from 'vue'

const { t, locale } = useI18n()
const router = useRouter()
const flowStore = useFlowStore()

// Список полисов, полученных с бэкенда
const policies = ref<Array<{ title: string; description: string; price?: number }>>([])
const loading = ref(true)
const error = ref<string | null>(null)
const selectedIdx = ref<number | null>(null)
const isChosen = computed(() => selectedIdx.value !== null)

onMounted(async () => {
    try {
        const response = await fetch('http://localhost:8000/insurance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lang: locale.value }),
        })

        if (!response.ok) throw new Error(`HTTP ${response.status}`)

        const data = await response.json()
        // API возвращает объект с числовыми ключами, переводим в массив
        policies.value = Object.values(data)
    } catch (e) {
        // eslint-disable-next-line no-console
        console.error(e)
        error.value = 'Failed to load policies'
    } finally {
        loading.value = false
    }
})

function selectPolicy(index: number) {
    selectedIdx.value = index
    const policy = policies.value[index]
    // Сохраняем выбранный полис в store для дальнейшего использования
    flowStore.formPolicy = {
        title: policy.title,
        price: policy.price,
    }
}

function back() {
    router.push('/') // возврат на Welcome.vue
}

function next() {
    if (!isChosen.value) {
        error.value = 'Please select a policy first'
        return
    }
    router.push('/contact_info') // переход на ContactInfo.vue
}

</script>

<template>
  <div class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8">
    <main class="flex flex-col items-center justify-center text-center space-y-6 max-w-2xl flex-1 w-full">
      <img src="/logo_ing.svg" alt="Ingosstrakh logo"
                class="w-60 h-auto my-6 ml-14 select-none pointer-events-none self-start" />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl whitespace-pre-line">
        {{ t('choose_policy.title') }}
      </h1>

      <div v-if="loading" class="text-gray-500 text-sm mt-8">Loading…</div>
      <div v-else-if="error" class="text-red-600 text-sm mt-8">{{ error }}</div>

      <div v-else class="w-full flex flex-col items-center space-y-4">
        <button
          v-for="(policy, idx) in policies"
          :key="idx"
          @click="selectPolicy(idx)"
          class="w-full max-w-xl text-left border rounded-2xl p-4 shadow-sm transition-all"
          :class="{
            'bg-blue-50 border-blue-500 ring-2 ring-blue-500': idx === selectedIdx,
            'bg-white border-gray-300 hover:bg-gray-50': idx !== selectedIdx,
          }"
        >
          <h2 class="font-semibold text-lg mb-2">{{ policy.title }}</h2>
          <p class="text-sm text-gray-700 whitespace-pre-line">{{ policy.description }}</p>
          <p class="text-sm text-gray-700 whitespace-pre-line" v-if="policy.price !== undefined">
            {{ policy.price }} ₽
          </p>
        </button>
      </div>
    </main>

    <div class="w-full max-w-xl flex justify-between gap-4 mt-6">
      <button
        @click="back"
        class="flex-1 rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
      >
        {{ t('choose_policy.back') }}
      </button>

      <button
        @click="next"
        :disabled="!isChosen"
        class="flex-1 rounded-2xl py-4 px-6 text-lg font-semibold shadow-lg transition-all"
        :class="isChosen ? 'bg-blue-600 text-white hover:bg-blue-700 active:shadow-none' : 'bg-blue-200 text-white opacity-60 cursor-not-allowed'"
      >
        {{ t('choose_policy.next') }}
      </button>
    </div>
  </div>
</template>