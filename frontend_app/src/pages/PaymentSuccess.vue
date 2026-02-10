<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFlowStore } from "@/store";
import { downloadPolicyById } from "@/services/api";

const { t } = useI18n();
const router = useRouter();
const flow = useFlowStore();

const generating = ref(false);

async function generateAndDownloadPolicy() {
  if (generating.value || !flow.policyId) return;
  generating.value = true;

  try {
    const blob = await downloadPolicyById(flow.policyId);

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `policy-${flow.policyId}.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (e) {
    console.error(e);
    alert(e && e.message ? e.message : "Ошибка генерации полиса");
  } finally {
    generating.value = false;
  }
}

function done() {
  // pinia store reset available as $reset
  if (flow.$reset) flow.$reset();
  router.push("/");
}
</script>

<template>
  <div
    class="flex flex-col items-center min-h-screen bg-gradient-to-b from-sky-50 to-white px-4 py-8"
  >
    <main
      class="flex flex-col items-center justify-center text-center space-y-6 max-w-xl flex-1 w-full"
    >
      <img
        src="/logo_ing.svg"
        alt="Ingosstrakh logo"
        class="w-60 h-auto my-6 ml-22 select-none pointer-events-none self-start"
      />
      <h1 class="font-extrabold leading-tight text-3xl sm:text-4xl md:text-5xl">
        {{ t("payment_success.title") }}
      </h1>

      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_1") }} {{ flow.formContacts.email }}
      </p>
      <p class="text-lg text-gray-700 max-w-md">
        {{ t("payment_success.text_2") }}
      </p>

      <button
        @click="generateAndDownloadPolicy"
        :disabled="generating"
        class="w-full max-w-xs rounded-2xl bg-white border-2 border-gray-300 py-4 px-6 text-gray-900 text-lg font-semibold shadow hover:bg-gray-50 active:shadow-none transition-all disabled:opacity-60"
      >
        {{
          generating
            ? t("payment_success.generating")
            : t("payment_success.download")
        }}
      </button>
    </main>

    <button
      @click="done"
      class="w-full max-w-xs rounded-2xl bg-blue-600 py-4 px-6 text-white text-lg font-semibold shadow-lg hover:bg-blue-700 active:shadow-none transition-all"
    >
      {{ t("payment_success.done") }}
    </button>
  </div>
</template>
