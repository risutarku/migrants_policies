<!-- =================================================== -->
<!-- ScanDocument.vue                                     -->
<!-- =================================================== -->

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useFlowStore } from '@/store'

const { t } = useI18n()
const router = useRouter()
const flow = useFlowStore()

const scanning = ref(false)
const overlayVisible = ref(false)

onMounted(() => {
    // 2 секундная пауза перед имитацией сканирования
    setTimeout(startScan, 2000)
})

async function startScan() {
    overlayVisible.value = true
    scanning.value = true
    try {
        const res = await fetch('http://localhost:8000/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
            // body: JSON.stringify({}) // добавьте тело запроса при необходимости
        })
        const data = await res.json()
        flow.formData = { ...flow.formData, ...data }
    } catch (e) {
        console.error(e)
    } finally {
        scanning.value = false
        // убираем полосу через 1.5 с
        setTimeout(() => (overlayVisible.value = false), 1500)
        router.push('/edit') // переход на EditData.vue
    }
}

function back() {
    router.back()
}
</script>
<template>
  <div class="relative flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8 overflow-hidden">
    <main class="flex flex-col items-center justify-center text-center space-y-8 max-w-2xl flex-1 w-full">
      <img src="/logo_ing.svg" alt="Ingosstrakh logo"
                class="w-60 h-auto my-6 ml-14 select-none pointer-events-none self-start" />
            <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl whitespace-pre-line">
                {{ t('scan_document.title') }}
            </h1>
      <img src="/scan_document.png" alt="scan" class="w-120 h-auto pointer-events-none select-none" />
    </main>

    <!-- Scanning stripe overlay -->
    <div v-if="overlayVisible" class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-2 bg-blue-500 animate-scan-strip"></div>
    </div>

    <button @click="back" class="w-full max-w-xs rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all">
      {{ t('scan_document.back') }}
    </button>
  </div>
</template>

<style scoped>
@keyframes scan {
    0% {
        transform: translateY(-100%);
    }

    100% {
        transform: translateY(100vh);
    }
}

.animate-scan-strip {
    animation: scan 1.5s linear forwards;
}
</style>

