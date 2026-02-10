<!-- src/pages/Confirm.vue -->
<script setup>
import { useFlowStore } from "@/store"; // можно через @
import { useRouter } from "vue-router";
import { makeInitPayload } from "@/utils/toBackend";
import { initPayment } from "@/services/api";

const store = useFlowStore();
const router = useRouter();
const amount = 1000; // копейки / тиыны

async function pay() {
  try {
    const payload = makeInitPayload(store.formData, amount);
    const { session_id } = await initPayment(payload);
    store.sessionId = session_id;
    router.push("/payment");
  } catch (e) {
    console.error("initPayment failed", e);
    // optional: показать toast/alert
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen gap-6">
    <!-- при желании: показать сводку данных -->
    <button class="btn" @click="pay">{{ $t("pay") }}</button>
  </div>
</template>

<style scoped lang="postcss">
@reference "../assets/tailwind.css";
.btn {
  @apply px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700;
}
</style>
