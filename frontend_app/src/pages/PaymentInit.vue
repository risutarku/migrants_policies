<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const price = computed(() => flow.formPolicy.price);
const loading = ref(false); // блокирует кнопку
const polling = ref(false); // показывает анимацию ожидания
let pollIv: ReturnType<typeof setInterval> | null = null;
let pollTo: ReturnType<typeof setTimeout> | null = null;

onUnmounted(() => {
  // чистим таймеры при уходе
  if (pollIv) clearInterval(pollIv);
  if (pollTo) clearTimeout(pollTo);
});

async function payByCard() {
  if (loading.value) return;
  loading.value = true;
  try {
    if (!flow.sessionID) flow.sessionID = crypto.randomUUID();
    const idempotencyKey = crypto.randomUUID();

    const payload = {
      session_id: flow.sessionID,
      idempotency_key: idempotencyKey,
      contacts: { ...flow.formContacts },
      policy: { title: flow.formPolicy.title, amount: flow.formPolicy.price },
      user: { ...flow.formData },
      arrived_for_hire: flow.arrived_for_hire,
    };

    const res = await fetch("http://localhost:8000/payment/init", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": idempotencyKey,
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json(); // { session_id, amount, currency }
    flow.sessionID = data.session_id;

    // 🔄 запускаем поллинг статуса
    await pollStatus(data.session_id, idempotencyKey);
  } catch (e) {
    console.error(e);
    alert(t("payment_init.error"));
  } finally {
    loading.value = false;
  }
}

function pollStatus(sessionId: string, key: string) {
  return new Promise<void>((resolve, reject) => {
    polling.value = true;

    pollIv = setInterval(async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/payment/status/${sessionId}`,
          {
            headers: { "Idempotency-Key": key },
          },
        );
        if (!res.ok) throw new Error("status HTTP " + res.status);
        const st = await res.json(); // { status, tx_id }
        if (st.status === "success") {
          cleanup();
          flow.txId = st.tx_id;
          router.push("/payment_success");
          resolve();
        }
      } catch (err) {
        console.error(err);
      }
    }, 2000); // каждые 2 с

    // стопим через 10 с
    pollTo = setTimeout(() => {
      cleanup();
      alert(t("payment_init.timeout"));
      reject(new Error("timeout"));
    }, 10_000);

    function cleanup() {
      polling.value = false;
      if (pollIv) {
        clearInterval(pollIv);
        pollIv = null;
      }
      if (pollTo) {
        clearTimeout(pollTo);
        pollTo = null;
      }
    }
  });
}

function back() {
  if (loading.value || polling.value) return;
  router.back();
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-8 max-w-xl flex-1 w-full"
    >
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-0 select-none pointer-events-none self-start"
      />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
        {{ t("payment_init.title") }}
      </h1>
      <h2 class="text-2xl font-semibold text-blue-600">
        {{ price.toLocaleString() }} ₽
      </h2>
      <img
        src="/sbp.png"
        alt="Ingosstrakh logo"
        class="w-100 h-auto my-6 select-none pointer-events-none self-start"
      />
      <div class="w-full grid gap-4 grid-cols-1 sm:grid-cols-2">
        <!-- Кредитная карта -->
        <button
          @click="payByCard"
          :disable="loading"
          class="flex flex-col items-center justify-center gap-2 rounded-2xl border-2 p-6 shadow-sm transition-all w-full"
          :class="
            loading
              ? 'border-blue-500 bg-blue-50 opacity-60 cursor-wait'
              : 'border-gray-300 bg-white hover:bg-gray-50'
          "
        >
          <img src="/icons/card.svg" alt="card" class="w-8 h-8" />
          <span class="font-medium">{{ t("payment_init.credit_card") }}</span>
        </button>
        <!-- Наличные -->
        <button
          class="flex flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-300 p-6 bg-white shadow-sm"
        >
          <img src="/icons/cash.svg" alt="cash" class="w-8 h-8" />
          <span class="font-medium">{{ t("payment_init.cash") }}</span>
        </button>
      </div>
    </main>

    <!-- Back button -->
    <button
      @click="back"
      class="w-full max-w-xs rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
    >
      {{ t("payment_init.back") }}
    </button>
  </div>
</template>

<style scoped>
.spinner {
  width: 48px;
  height: 48px;
  border: 6px solid #93c5fd; /* blue-300 */
  border-top-color: #2563eb; /* blue-600 */
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
