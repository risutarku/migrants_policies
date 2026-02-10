<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { initPayment, getPaymentStatus } from "@/services/api";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const price = computed(() => flow.formPolicy.price);
const loading = ref(false);
const polling = ref(false);
let pollIv = null;
let pollTo = null;

onUnmounted(() => {
  if (pollIv) clearInterval(pollIv);
  if (pollTo) clearTimeout(pollTo);
});

async function payByCard() {
  if (loading.value) return;
  if (!flow.policyId) {
    alert(t("payment_init.no_policy"));
    return;
  }

  loading.value = true;

  try {
    if (!flow.sessionId) flow.sessionId = crypto.randomUUID();
    const idempotencyKey = crypto.randomUUID();

    const data = await initPayment({
      policy_id: flow.policyId,
      session_id: flow.sessionId,
      idempotency_key: idempotencyKey,
    });

    flow.sessionId = data.session_id;

    await pollStatus(flow.sessionId);
  } catch (e) {
    console.error(e);
    alert(t("payment_init.error"));
  } finally {
    loading.value = false;
  }
}

function pollStatus(sessionId) {
  return new Promise((resolve, reject) => {
    polling.value = true;

    pollIv = setInterval(async () => {
      try {
        const st = await getPaymentStatus(sessionId);
        if (st.status === "success") {
          cleanup();
          flow.txId = st.tx_id;
          router.push("/payment_success");
          resolve();
        }
        if (st.status === "failed") {
          cleanup();
          alert(t("payment_init.failed"));
          reject(new Error("failed"));
        }
      } catch (err) {
        console.error(err);
      }
    }, 2000);

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
        {{ Number(price || 0).toLocaleString() }} ₽
      </h2>

      <img
        src="/sbp.png"
        alt="SBP"
        class="w-100 h-auto my-6 select-none pointer-events-none"
      />

      <div class="w-full grid gap-4 grid-cols-1 sm:grid-cols-2">
        <button
          @click="payByCard"
          :disabled="loading"
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

        <button
          class="flex flex-col items-center justify-center gap-2 rounded-2xl border-2 border-gray-300 p-6 bg-white shadow-sm"
        >
          <img src="/icons/cash.svg" alt="cash" class="w-8 h-8" />
          <span class="font-medium">{{ t("payment_init.cash") }}</span>
        </button>
      </div>

      <div v-if="polling" class="text-sm text-gray-500">
        {{ t("payment_init.waiting") }}
      </div>
    </main>

    <button
      @click="back"
      class="w-full max-w-xs rounded-2xl bg-gray-200 py-4 px-6 text-gray-800 text-lg font-semibold shadow hover:bg-gray-300 active:shadow-none transition-all"
    >
      {{ t("payment_init.back") }}
    </button>
  </div>
</template>
